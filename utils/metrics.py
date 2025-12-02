import numpy as np
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    roc_auc_score,
    precision_recall_curve,
    auc,
    balanced_accuracy_score,
    recall_score
)


def compute_all_metrics(y_true, y_pred, y_prob):
    """
    Returns a dictionary of ALL important metrics.
    """

    accuracy = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    f1_macro = f1_score(y_true, y_pred, average="macro", zero_division=0)
    f1_weighted = f1_score(y_true, y_pred, average="weighted", zero_division=0)

    # ROC-AUC
    try:
        roc_auc = roc_auc_score(y_true, y_prob)
    except:
        roc_auc = 0.5

    # PR-AUC
    try:
        precision, recall, _ = precision_recall_curve(y_true, y_prob)
        pr_auc = auc(recall, precision)
    except:
        pr_auc = 0.5

    # Balanced Acc
    bal_acc = balanced_accuracy_score(y_true, y_pred)

    # Sensitivity (Recall of positive class)
    sens = recall_score(y_true, y_pred, pos_label=1, zero_division=0)

    # Specificity (Recall of negative class)
    spec = recall_score(y_true, y_pred, pos_label=0, zero_division=0)

    return {
        "accuracy": accuracy,
        "f1": f1,
        "f1_macro": f1_macro,
        "f1_weighted": f1_weighted,
        "auc": roc_auc,
        "pr_auc": pr_auc,
        "balanced_accuracy": bal_acc,
        "sensitivity": sens,
        "specificity": spec
    }
