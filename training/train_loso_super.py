import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.utils.data import DataLoader

from model.etlaf_supermodel import ETLAFSuperModel
from dataset.super_dataset import SuperDataset


def make_dataloader(train_subjects, raw_data, mb_data, labels, device, batch_size=2):
    ds = SuperDataset(train_subjects, raw_data, mb_data, labels, device)
    return DataLoader(ds, batch_size=batch_size, shuffle=True)


def train_one_subject_super(
    train_subjects,
    test_subject,
    raw_data,
    mb_data,
    labels,
    device,
    epochs=12,
    lr=1e-4
):
    """
    LOSO training for ETLAF super-model.
    """
    print(f"\n🚀 Training SUPERMODEL for test subject: {test_subject}")

    model = ETLAFSuperModel().to(device)

    optimizer = AdamW(model.parameters(), lr=lr, weight_decay=1e-5)
    criterion = nn.BCEWithLogitsLoss()

    train_loader = make_dataloader(train_subjects, raw_data, mb_data, labels, device)

    for epoch in range(epochs):
        model.train()
        total_loss = 0.0

        for raw_batch, mb_batch, y_batch in train_loader:
            raw_batch = raw_batch.to(device)
            mb_batch = mb_batch.to(device)
            y_batch = y_batch.to(device)

            optimizer.zero_grad()

            logits = model(raw_batch, mb_batch).squeeze()
            loss = criterion(logits, y_batch)

            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch+1}/{epochs} | Loss: {total_loss/len(train_loader):.4f}")

    return model
