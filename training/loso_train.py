import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler
import numpy as np
import random
import time
from model.brain2vec import Brain2Vec


# ============================================================
# Subject Dataset
# ============================================================
class SubjectDataset(Dataset):
    def __init__(self, data_dict, label_dict, subjects):
        self.samples = []
        self.labels = []

        for s in subjects:
            trials = data_dict[s]          # list of (32, W, 128)
            lbls = label_dict[s]           # list of labels

            for x, y in zip(trials, lbls):
                self.samples.append(torch.tensor(x, dtype=torch.float32))
                self.labels.append(float(y))

        self.labels = torch.tensor(self.labels).float()

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        X = self.samples[idx]     # (32, W, 128)
        y = self.labels[idx]
        return X, y.unsqueeze(0)


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

    torch.manual_seed(42)
    np.random.seed(42)
    random.seed(42)

    train_dataset = SubjectDataset(data, labels, train_subjects)
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
        batch_size=8,      # smaller batch because shape is larger
        sampler=sampler,
        num_workers=0,     # set to 0 on Windows
        pin_memory=False
    )

    model = Brain2Vec().to(device)
    optimizer = optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-4)

    pos_weight = torch.tensor([3.0], device=device)
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)

    EPOCHS = 12
    early_stopper = EarlyStopper(patience=3)

    print(f"\n🚀 Training LOSO: Test on {test_subject}")

    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0
        start = time.time()

        for X, y in train_loader:
            X = X.to(device)    # (B, 32, W, 128)
            y = y.to(device)

            optimizer.zero_grad()

            out = model(X)
            loss = criterion(out, y)

            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(train_loader)
        print(f"Epoch {epoch+1}/{EPOCHS} | Loss: {avg_loss:.4f} | Time: {time.time()-start:.1f}s")

        if early_stopper.should_stop(avg_loss):
            print("🛑 Early stopping.")
            break

    return model
