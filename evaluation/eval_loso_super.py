import torch
import numpy as np
from utils.metrics import compute_all_metrics


def evaluate_one_subject_super(
    model,
    test_subject,
    raw_data,
    mb_data,
    labels,
    device
):
    """
    Evaluate ETLAF supermodel on ONE subject (LOSO).
    """
    model.eval()

    preds = []
    probs = []
    trues = []

    raw_trials = raw_data[test_subject]
    mb_trials = mb_data[test_subject]
    gt_labels = labels[test_subject]

    for i in range(len(raw_trials)):
        raw = torch.tensor(raw_trials[i], dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(device)
        mb  = torch.tensor(mb_trials[i], dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(device)

        with torch.no_grad():
            logit = model(raw, mb).item()
            p = torch.sigmoid(torch.tensor(logit)).item()
            pred = 1 if p >= 0.5 else 0

        preds.append(pred)
        probs.append(p)
        trues.append(gt_labels[i])

    return compute_all_metrics(
        np.array(trues),
        np.array(preds),
        np.array(probs)
    )
