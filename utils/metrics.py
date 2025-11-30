from sklearn.metrics import accuracy_score, f1_score, roc_auc_score


def compute_metrics(y_true, preds, probs):
    acc = accuracy_score(y_true, preds)
    f1 = f1_score(y_true, preds, zero_division=0)

    try:
        auc = roc_auc_score(y_true, probs)
    except:
        auc = 0.5

    return acc, f1, auc
