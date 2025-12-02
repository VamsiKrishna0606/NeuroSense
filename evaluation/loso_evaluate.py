import torch
import numpy as np
from utils.metrics import compute_all_metrics


def evaluate_subject(model, test_subject, data, labels, device):

    model.eval()
    all_preds = []
    all_probs = []
    all_true = []

    # iterate all 40 trials of that subject
    for i in range(len(data[test_subject])):

        X = data[test_subject][i]

        # Convert to tensor
        if isinstance(X, np.ndarray):
            X = torch.tensor(X, dtype=torch.float32)

        X = X.unsqueeze(0).to(device)     # (1, 32, W, 128)

        with torch.no_grad():
            logits = model(X).squeeze()
            prob = torch.sigmoid(logits).item()
            pred = 1 if prob >= 0.5 else 0

        all_probs.append(prob)
        all_preds.append(pred)
        all_true.append(labels[test_subject][i])

    # Compute all metrics
    return compute_all_metrics(
        np.array(all_true),
        np.array(all_preds),
        np.array(all_probs)
    )
