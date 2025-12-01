from preprocessing.deap_subject_loader import load_all_subjects
from training.loso_train import train_one_subject
from evaluation.loso_evaluate import evaluate_subject

import torch
import numpy as np
import csv
import os
import time


if __name__ == "__main__":

    print("\n==============================")
    print("   LOADING DEAP SUBJECT DATA")
    print("==============================")

    data_path = "data/deap"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    data, labels = load_all_subjects(data_path)
    subjects = sorted(data.keys())

    os.makedirs("results", exist_ok=True)
    results_file = "results/summary.csv"

    # ---------------------------------------------------------
    # CSV HEADER
    # ---------------------------------------------------------
    with open(results_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "subject",
            "accuracy",
            "f1",
            "f1_macro",
            "f1_weighted",
            "auc",
            "pr_auc",
            "balanced_accuracy",
            "sensitivity",
            "specificity",
            "best_threshold"
        ])

    all_metrics = {k: [] for k in [
        "accuracy",
        "f1",
        "f1_macro",
        "f1_weighted",
        "auc",
        "pr_auc",
        "balanced_accuracy",
        "sensitivity",
        "specificity"
    ]}

    print("\n==============================")
    print("        STARTING LOSO")
    print("==============================")

    total_start = time.time()

    # ---------------------------------------------------------
    # LOSO LOOP
    # ---------------------------------------------------------
    for test_subject in subjects:

        print(f"\n-----------------------------------------------")
        print(f"🧪 TEST SUBJECT: {test_subject}")
        print(f"-----------------------------------------------")

        train_subjects = [s for s in subjects if s != test_subject]

        # Train
        model = train_one_subject(train_subjects, test_subject, data, labels, device)

        # Evaluate
        metrics = evaluate_subject(model, test_subject, data, labels, device)

        # Log metrics
        with open(results_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                test_subject,
                metrics["accuracy"],
                metrics["f1"],
                metrics["f1_macro"],
                metrics["f1_weighted"],
                metrics["auc"],
                metrics["pr_auc"],
                metrics["balanced_accuracy"],
                metrics["sensitivity"],
                metrics["specificity"],
                metrics["best_threshold"]
            ])

        # Append for averaging later
        for k in all_metrics.keys():
            all_metrics[k].append(metrics[k])

        print(f"✔ ACC={metrics['accuracy']:.3f} | "
              f"F1={metrics['f1']:.3f} | "
              f"AUC={metrics['auc']:.3f} | "
              f"PR-AUC={metrics['pr_auc']:.3f} | "
              f"Thr={metrics['best_threshold']:.2f}")

    # ---------------------------------------------------------
    # FINAL AVERAGES
    # ---------------------------------------------------------
    print("\n==============================")
    print("        FINAL LOSO RESULTS")
    print("==============================")

    for k in all_metrics:
        print(f"{k}: {np.mean(all_metrics[k]):.4f}")

    print("\n==============================")
    print("        EXPERIMENT COMPLETE")
    print("==============================")
    print(f"Total Time: {time.time() - total_start:.1f} seconds")
