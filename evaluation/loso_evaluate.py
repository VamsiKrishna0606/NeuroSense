import torch
import numpy as np
from utils.metrics import compute_metrics


def evaluate_subject(model, test_subject, data, labels, device):

    model.eval()
    X = torch.stack(data[test_subject]).to(device)
    y_true = torch.tensor(labels[test_subject]).long().numpy()

    with torch.no_grad():
        logits = model(X).squeeze()
        probs = torch.sigmoid(logits).cpu().numpy()
        preds = (probs >= 0.5).astype(int)

    acc, f1, auc = compute_metrics(y_true, preds, probs)
    return acc, f1, auc
