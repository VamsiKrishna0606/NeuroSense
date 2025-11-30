import torch
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from torch.utils.data import Dataset, DataLoader
import os
from utils.metrics import save_subject_results

class TestDataset(Dataset):
    def __init__(self, subject_data, subject_labels, subject):
        self.samples = subject_data[subject]
        self.labels = subject_labels[subject]

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx], torch.tensor(self.labels[idx]).float()

def evaluate_subject(model, subject, data, labels, device):

    test_dataset = TestDataset(data, labels, subject)
    loader = DataLoader(test_dataset, batch_size=16)

    all_labels = []
    all_preds = []
    all_probs = []

    model.eval()
    with torch.no_grad():
        for X, y in loader:
            X = X.to(device)

            out = model(X).squeeze()
            probs = torch.sigmoid(out)

            preds = (probs >= 0.5).float()

            all_labels.extend(y.numpy())
            all_preds.extend(preds.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())

    acc = accuracy_score(all_labels, all_preds)
    f1 = f1_score(all_labels, all_preds)
    auc = roc_auc_score(all_labels, all_probs)

    save_subject_results(subject, all_labels, all_preds, all_probs)

    return acc, f1, auc
