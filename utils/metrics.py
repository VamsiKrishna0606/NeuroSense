import os
import numpy as np
import csv
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

def save_subject_results(subject, labels, preds, probs):

    os.makedirs(f"results/{subject}", exist_ok=True)

    # Save predictions CSV
    with open(f"results/{subject}/predictions.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["true", "pred", "prob"])
        for t, p, pr in zip(labels, preds, probs):
            writer.writerow([t, p, pr])

    # Confusion matrix
    cm = confusion_matrix(labels, preds)

    plt.figure(figsize=(3,3))
    plt.imshow(cm, cmap="Blues")
    plt.title(f"Confusion Matrix — {subject}")
    plt.colorbar()
    plt.savefig(f"results/{subject}/confusion_matrix.png")
    plt.close()
