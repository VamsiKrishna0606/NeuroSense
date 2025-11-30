from preprocessing.deap_subject_loader import DEAPSubjectLoader
from training.loso_train import train_one_subject
from evaluation.loso_evaluate import evaluate_subject

import torch
import numpy as np
import csv
import os

if __name__ == "__main__":
    data_path = "data/deap"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    loader = DEAPSubjectLoader(data_path)

    subjects = sorted(loader.data.keys())   # ["s01" ... "s32"]

    os.makedirs("results", exist_ok=True)
    results_file = "results/summary.csv"

    with open(results_file, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["subject", "accuracy", "f1", "auc"])

    all_acc, all_f1, all_auc = [], [], []

    for test_subject in subjects:
        train_subjects = [s for s in subjects if s != test_subject]

        model = train_one_subject(
            train_subjects,
            test_subject,
            loader.data,
            loader.labels,
            device
        )

        acc, f1, auc = evaluate_subject(
            model,
            test_subject,
            loader.data,
            loader.labels,
            device
        )

        all_acc.append(acc)
        all_f1.append(f1)
        all_auc.append(auc)

        with open(results_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([test_subject, acc, f1, auc])

        print(f"\n🧪 {test_subject} — ACC={acc:.3f}, F1={f1:.3f}, AUC={auc:.3f}")

    print("\n======================")
    print("  FINAL LOSO RESULTS")
    print("======================")
    print(f"Avg Accuracy: {np.mean(all_acc):.3f}")
    print(f"Avg F1: {np.mean(all_f1):.3f}")
    print(f"Avg AUC: {np.mean(all_auc):.3f}")
