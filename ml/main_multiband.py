from preprocessing.deap_multiband import load_multiband_dataset
from training.loso_train_multiband import train_one_subject_multiband
from evaluation.loso_evaluate_multiband import evaluate_subject_multiband

import numpy as np
import csv
import torch
import time


if __name__ == "__main__":
    print("\n==============================")
    print("    LOADING MULTIBAND DATA")
    print("==============================")

    data_path = "data/deap"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    data, labels = load_multiband_dataset(data_path)
    subjects = sorted(data.keys())

    print("Loaded subjects:", len(subjects))

    # RESULTS CSV
    with open("results/multiband_summary.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "subject", "accuracy", "f1", "f1_macro", "f1_weighted",
            "auc", "pr_auc", "balanced_accuracy",
            "sensitivity", "specificity"
        ])

    print("\n==============================")
    print("       STARTING LOSO")
    print("==============================")

    for test_sub in subjects:
        print("\n--------------------------------")
        print(f"🧪 TEST SUBJECT: {test_sub}")
        print("--------------------------------")

        train_subs = [s for s in subjects if s != test_sub]

        model = train_one_subject_multiband(train_subs, test_sub, data, labels, device)

        metrics = evaluate_subject_multiband(model, test_sub, data, labels, device)

        print(f"✔ ACC={metrics['accuracy']:.3f} "
              f"| F1={metrics['f1']:.3f} "
              f"| AUC={metrics['auc']:.3f} "
              f"| PR-AUC={metrics['pr_auc']:.3f}")

        with open("results/multiband_summary.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                test_sub,
                metrics["accuracy"],
                metrics["f1"],
                metrics["f1_macro"],
                metrics["f1_weighted"],
                metrics["auc"],
                metrics["pr_auc"],
                metrics["balanced_accuracy"],
                metrics["sensitivity"],
                metrics["specificity"],
            ])

    print("\n==============================")
    print("         EXPERIMENT DONE")
    print("==============================")
