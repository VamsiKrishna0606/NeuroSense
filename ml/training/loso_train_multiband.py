import torch
import torch.nn as nn
from torch.optim import Adam
from model.brain2vec_multiband import Brain2Vec_MultiBand
from torch.utils.data import DataLoader
import numpy as np
import time

# NEW IMPORT
from preprocessing.multiband_dataset import MultibandDataset


def make_dataloader(train_subjects, data, labels, device):
    """
    FIXED: Uses streaming dataset instead of loading entire 5GB tensor.
    """
    dataset = MultibandDataset(train_subjects, data, labels, device)
    return DataLoader(dataset, batch_size=2, shuffle=True)  # BATCH SIZE = 2 🧠


def train_one_subject_multiband(train_subjects, test_subject, data, labels, device):

    model = Brain2Vec_MultiBand().to(device)
    optimizer = Adam(model.parameters(), lr=1e-4, weight_decay=1e-5)
    criterion = nn.BCEWithLogitsLoss()

    train_loader = make_dataloader(train_subjects, data, labels, device)

    print(f"🚀 Training Multiband LOSO: Test on {test_subject}")

    for epoch in range(12):
        start = time.time()
        model.train()

        losses = []

        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()

            logits = model(X_batch).squeeze()

            loss = criterion(logits, y_batch)
            loss.backward()
            optimizer.step()

            losses.append(loss.item())

        print(f"Epoch {epoch+1}/12 | Loss: {np.mean(losses):.4f} | Time: {time.time()-start:.1f}s")

    return model
