import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

from model.brain2vec import Brain2Vec


class SubjectDataset(Dataset):
    def __init__(self, data_dict, label_dict, subjects):
        self.samples = []
        self.labels = []

        for s in subjects:
            self.samples.extend(data_dict[s])
            self.labels.extend(label_dict[s])

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx], torch.tensor(self.labels[idx]).float()


def train_one_subject(train_subjects, test_subject, data, labels, device):

    train_dataset = SubjectDataset(data, labels, train_subjects)
    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)

    model = Brain2Vec().to(device)
    optimizer = optim.Adam(model.parameters(), lr=1e-4)
    pos_weight = torch.tensor([3.0], device=device)
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)

    EPOCHS = 20

    print(f"\n🚀 Training LOSO — Test on {test_subject} | Train on {len(train_subjects)} subjects")

    for epoch in range(EPOCHS):
        total_loss = 0
        model.train()

        for X, y in train_loader:
            X, y = X.to(device), y.to(device).unsqueeze(1)

            optimizer.zero_grad()
            out = model(X)
            loss = criterion(out, y)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch+1}/{EPOCHS} | Loss: {total_loss:.4f}")

    return model
