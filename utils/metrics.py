from sklearn.metrics import (
    accuracy_score,
    f1_score,
    roc_auc_score,
    precision_recall_curve,
    auc,
    balanced_accuracy_score,
    confusion_matrix
)
import numpy as np


def compute_all_metrics(y_true, preds, probs):
    """
    y_true: (N,)
    preds: (N,)
    probs: (N,)  raw probabilities (sigmoid outputs)
    """

    # -----------------------------------------------------------
    # Standard Metrics
    # -----------------------------------------------------------
    acc = accuracy_score(y_true, preds)
    f1 = f1_score(y_true, preds, zero_division=0)

    # Macro and weighted F1 for imbalanced cases
    f1_macro = f1_score(y_true, preds, average='macro', zero_division=0)
    f1_weighted = f1_score(y_true, preds, average='weighted', zero_division=0)

    # -----------------------------------------------------------
    # AUC (Safe)
    # -----------------------------------------------------------
    try:
        auc_roc = roc_auc_score(y_true, probs)
    except:
        auc_roc = 0.5

    # -----------------------------------------------------------
    # PR-AUC (important when F1 is weak)
    # -----------------------------------------------------------
    try:
        precision, recall, _ = precision_recall_curve(y_true, probs)
        pr_auc = auc(recall, precision)
    except:
        pr_auc = 0.0

    # -----------------------------------------------------------
    # Balanced Accuracy
    # -----------------------------------------------------------
    try:
        bal_acc = balanced_accuracy_score(y_true, preds)
    except:
        bal_acc = acc

    # -----------------------------------------------------------
    # Sensitivity & Specificity
    # -----------------------------------------------------------
    try:
        tn, fp, fn, tp = confusion_matrix(y_true, preds).ravel()

        sensitivity = tp / (tp + fn + 1e-6)  # recall for positive class
        specificity = tn / (tn + fp + 1e-6)  # recall for negative class
    except:
        sensitivity, specificity = 0.0, 0.0

    return {
        "accuracy": acc,
        "f1": f1,
        "f1_macro": f1_macro,
        "f1_weighted": f1_weighted,
        "auc": auc_roc,
        "pr_auc": pr_auc,
        "balanced_accuracy": bal_acc,
        "sensitivity": sensitivity,
        "specificity": specificity
    }


# =============================================================
# Keep backwards compatibility with your old compute_metrics()
# =============================================================
def compute_metrics(y_true, preds, probs):
    m = compute_all_metrics(y_true, preds, probs)
    return m["accuracy"], m["f1"], m["auc"]
