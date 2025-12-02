import torch
import csv
import time

from preprocessing.deap_loader_super import load_super_deap
from training.train_loso_super import train_one_subject_super
from evaluation.eval_loso_super import evaluate_one_subject_super


if __name__ == "__main__":
    print("\n==============================")
    print("      LOADING SUPER DATA")
    print("==============================")

    data_path = "data/deap"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    raw_data, mb_data, labels = load_super_deap(data_path)

    subjects = sorted(raw_data.keys())
    print(f"✔ Loaded {len(subjects)} subjects.")

    # ----------------------------------------------------------------------
    # CSV LOGGING
    # ----------------------------------------------------------------------
    with open("results/supermodel_summary.csv", "w", newline="") as f:
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
            "specificity"
        ])

    print("\n==============================")
    print("         STARTING LOSO")
    print("==============================")

    for test_subject in subjects:
        print("\n--------------------------------")
        print(f"🧪 TEST SUBJECT: {test_subject}")
        print("--------------------------------")

        train_subjects = [s for s in subjects if s != test_subject]

        # Train
        model = train_one_subject_super(
            train_subjects=train_subjects,
            test_subject=test_subject,
            raw_data=raw_data,
            mb_data=mb_data,
            labels=labels,
            device=device,
            epochs=12,
            lr=1e-4
        )

        # Evaluate
        metrics = evaluate_one_subject_super(
            model=model,
            test_subject=test_subject,
            raw_data=raw_data,
            mb_data=mb_data,
            labels=labels,
            device=device
        )

        print(f"✔ ACC={metrics['accuracy']:.3f} | "
              f"F1={metrics['f1']:.3f} | "
              f"AUC={metrics['auc']:.3f} | "
              f"PR-AUC={metrics['pr_auc']:.3f}")

        # Save
        with open("results/supermodel_summary.csv", "a", newline="") as f:
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
            ])

    print("\n==============================")
    print("        EXPERIMENT DONE")
    print("==============================")
