import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler

from model.brain2vec import Brain2Vec
import numpy as np
import random
import time


# ============================================================
# Subject Dataset
# ============================================================
class SubjectDataset(Dataset):
    def __init__(self, data_dict, label_dict, subjects):
        self.samples = []
        self.labels = []

        for s in subjects:
            self.samples.extend(data_dict[s])      # list of tensors
            self.labels.extend(label_dict[s])

        self.labels = torch.tensor(self.labels).float()

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        X = self.samples[idx]
        y = self.labels[idx]
        return X, y.unsqueeze(0)     # keep (1,) shape


# ============================================================
# Early Stopping
# ============================================================
class EarlyStopper:
    def __init__(self, patience=3, min_delta=1e-4):
        self.patience = patience
        self.min_delta = min_delta
        self.best_loss = float('inf')
        self.counter = 0

    def should_stop(self, val_loss):
        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
            return False
        else:
            self.counter += 1
            return self.counter >= self.patience


# ============================================================
# Main LOSO Training Function
# ============================================================
def train_one_subject(train_subjects, test_subject, data, labels, device):

    # ----------------------------------------------------------
    # Reproducibility
    # ----------------------------------------------------------
    torch.manual_seed(42)
    np.random.seed(42)
    random.seed(42)

    # ----------------------------------------------------------
    # Dataset + Balanced Sampler
    # ----------------------------------------------------------
    train_dataset = SubjectDataset(data, labels, train_subjects)

    # compute weights for balancing positives/negatives
    label_tensor = train_dataset.labels
    class_sample_counts = torch.tensor([(label_tensor == 0).sum(),
                                        (label_tensor == 1).sum()],
                                       dtype=torch.float)

    weights = 1.0 / class_sample_counts
    sample_weights = torch.tensor([weights[int(l)] for l in label_tensor])

    sampler = WeightedRandomSampler(
        weights=sample_weights,
        num_samples=len(sample_weights),
        replacement=True
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=16,
        sampler=sampler,
        num_workers=2,
        pin_memory=True
    )

    # ----------------------------------------------------------
    # Model + Optimizer + Scheduler
    # ----------------------------------------------------------
    model = Brain2Vec().to(device)
    optimizer = optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-4)

    # BCE loss but with pos_weight for extra influence on positives (boost F1)
    pos_weight = torch.tensor([3.0], device=device)
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)

    # Scheduler — reduce LR when training gets stuck
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode='min',
        patience=2,
        factor=0.5,
        verbose=False
    )

    EPOCHS = 15
    early_stopper = EarlyStopper(patience=3)

    print(f"\n🚀 Training LOSO: Test on {test_subject} | Train on {len(train_subjects)} subjects")

    # ----------------------------------------------------------
    # Training Loop
    # ----------------------------------------------------------
    for epoch in range(EPOCHS):

        start_time = time.time()
        model.train()
        total_loss = 0.0

        for X, y in train_loader:
            X = X.to(device)
            y = y.to(device)

            optimizer.zero_grad()

            out = model(X)
            loss = criterion(out, y)

            loss.backward()

            # gradient clipping prevents exploding gradients (common in LOSO)
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

            optimizer.step()
            total_loss += loss.item()

        avg_loss = total_loss / len(train_loader)
        scheduler.step(avg_loss)

        print(f"Epoch {epoch+1}/{EPOCHS} | Loss: {avg_loss:.4f} | LR: {optimizer.param_groups[0]['lr']:.6f} | Time: {time.time()-start_time:.1f}s")

        # early stopping
        if early_stopper.should_stop(avg_loss):
            print("🛑 Early stopping triggered.")
            break

    return model
