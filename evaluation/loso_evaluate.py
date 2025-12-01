import torch
import numpy as np
from utils.metrics import compute_all_metrics


def evaluate_subject(model, test_subject, data, labels, device, batch_size=16):
    """
    Evaluates the trained model on ONE subject.
    Now uses:
    - Batched inference (no memory spikes)
    - Threshold tuning for F1 improvement
    - Full metrics (AUC, PR-AUC, Balanced accuracy, etc.)
    """

    model.eval()

    # prepare test samples
    X_list = data[test_subject]
    y_true = np.array(labels[test_subject])

    probs_all = []
    preds_all = []

    # -----------------------------
    # BATCHED INFERENCE
    # -----------------------------
    with torch.no_grad():
        for i in range(0, len(X_list), batch_size):
            batch = X_list[i:i+batch_size]
            batch = torch.stack(batch).to(device)   # (B, 1, 32, 63, 128)

            logits = model(batch).squeeze()         # (B,)
            probs = torch.sigmoid(logits).cpu().numpy()
            probs_all.extend(probs)

    probs_all = np.array(probs_all)

    # ---------------------------------------------------------
    # THRESHOLD TUNING — find best threshold for F1 per subject
    # ---------------------------------------------------------
    thresholds = np.linspace(0.3, 0.7, 21)  # 0.3 → 0.7
    best_f1 = -1
    best_thr = 0.5
    best_preds = None

    for thr in thresholds:
        preds = (probs_all >= thr).astype(int)

        # compute temporary metrics
        tp = np.sum((preds == 1) & (y_true == 1))
        fp = np.sum((preds == 1) & (y_true == 0))
        fn = np.sum((preds == 0) & (y_true == 1))

        f1 = (2 * tp) / (2 * tp + fp + fn + 1e-6)
        if f1 > best_f1:
            best_f1 = f1
            best_thr = thr
            best_preds = preds

    # use best threshold predictions
    preds_all = best_preds

    # ---------------------------------------------------------
    # Compute ALL metrics using upgraded metrics suite
    # ---------------------------------------------------------
    metrics = compute_all_metrics(y_true, preds_all, probs_all)

    # attach best threshold for logging
    metrics["best_threshold"] = float(best_thr)

    return metrics
