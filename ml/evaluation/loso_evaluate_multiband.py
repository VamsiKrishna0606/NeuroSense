import torch
import numpy as np
from utils.metrics import compute_all_metrics

def evaluate_subject_multiband(model, test_subject, data, labels, device):
    model.eval()

    preds = []
    probs = []
    true_labels = []

    trials = data[test_subject]

    for i in range(len(trials)):
        X = trials[i]

        X = torch.tensor(X, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(device)
        # -> (1,1,32,60,4,128)

        with torch.no_grad():
            logit = model(X).item()
            p = torch.sigmoid(torch.tensor(logit)).item()
            pred = 1 if p >= 0.5 else 0

        preds.append(pred)
        probs.append(p)
        true_labels.append(labels[test_subject][i])

    return compute_all_metrics(
        np.array(true_labels),
        np.array(preds),
        np.array(probs)
    )
