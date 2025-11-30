import os
import scipy.io as sio
import torch
import numpy as np


def load_all_subjects(data_folder):
    """
    Loads all DEAP subjects into:
    data["s01"] = [tensor1, tensor2, ...]
    labels["s01"] = [0,1,0,1,...]
    """

    data = {}
    labels = {}

    print(f"📥 Loading DEAP subjects from: {data_folder}")

    files = sorted(os.listdir(data_folder))

    for file in files:
        if not file.endswith(".mat"):
            continue

        subject_id = file.replace(".mat", "")  # "s01"
        path = os.path.join(data_folder, file)

        mat = sio.loadmat(path, simplify_cells=True)
        eeg = mat["data"]        # shape: (40 trials, 40 channels, 8064 samples)
        lbl = mat["labels"]      # shape: (40 trials, 4 labels)

        subject_samples = []
        subject_labels = []

        arousal = lbl[:, 1]
        bin_labels = (arousal >= 5).astype(int)

        for i in range(40):

            trial = eeg[i][:32]  # take first 32 channels

            for c in range(32):
                ch = trial[c]
                ch = (ch - ch.mean()) / (ch.std() + 1e-6)
                trial[c] = ch

            # reshape: 8064 → (252, 32)
            reshaped = []
            for c in range(32):
                ch = trial[c].reshape(252, 32)
                reshaped.append(ch)

            reshaped = np.stack(reshaped)  # (32, 252, 32)
            reshaped = reshaped[:, :, 0]    # (32, 252)

            tensor = torch.tensor(reshaped, dtype=torch.float32).unsqueeze(0)
            subject_samples.append(tensor)
            subject_labels.append(int(bin_labels[i]))

        data[subject_id] = subject_samples
        labels[subject_id] = subject_labels

        print(f"  Loaded: {subject_id} → {len(subject_samples)} samples")

    print("✅ Finished loading all subjects.")
    return data, labels
