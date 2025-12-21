import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, WeightedRandomSampler, SubsetRandomSampler
from sklearn.model_selection import train_test_split

from preprocessing.deap_preprocess import DEAPDataset
from model.brain2vec import Brain2Vec


def train_model(data_path):

    print("\n==============================")
    print("   LOADING DEAP DATASET")
    print("==============================")

    dataset = DEAPDataset(data_path)

    # Convert labels properly
    labels = torch.tensor(dataset.labels).long()

    # Compute class weights
    class_counts = torch.bincount(labels)        # [count0, count1]
    class_weights = 1.0 / class_counts.float()
    sample_weights = class_weights[labels]

    # Balanced sampler
    sampler = WeightedRandomSampler(
        weights=sample_weights,
        num_samples=len(sample_weights),
        replacement=True
    )

    # Train / Test split
    indices = list(range(len(dataset)))
    train_idx, test_idx = train_test_split(indices, test_size=0.2, random_state=42)

    train_loader = DataLoader(dataset, batch_size=16, sampler=sampler)
    test_loader = DataLoader(dataset, batch_size=16, sampler=SubsetRandomSampler(test_idx))

    # Device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🖥  Using device: {device}")

    # Model
    model = Brain2Vec().to(device)

    # BCE with weighted positive class
    pos_weight = torch.tensor([3.5], device=device)
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)

    optimizer = optim.Adam(model.parameters(), lr=1e-4)
    EPOCHS = 30

    print("\n==============================")
    print("      TRAINING BRAIN2VEC")
    print("==============================\n")

    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0

        for X, y in train_loader:
            X = X.to(device)
            y = y.to(device).float().unsqueeze(1)

            optimizer.zero_grad()
            out = model(X)
            loss = criterion(out, y)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch+1}/{EPOCHS} | Loss = {total_loss:.4f}")

    # Save model
    os.makedirs("checkpoints", exist_ok=True)
    save_path = "checkpoints/brain2vec.pth"
    torch.save(model.state_dict(), save_path)

    print(f"\n💾 Model saved at: {save_path}")

    return save_path, test_loader
