import os
import numpy as np
import scipy.io as sio
import torch

class DEAPSubjectLoader:
    """
    Loads DEAP dataset subject-wise for LOSO.
    Output format:
        self.data["s01"] = [tensor, tensor, ...]  # 40 trials
        self.labels["s01"] = [0/1, 0/1, ...]      # 40 labels
    """

    def __init__(self, data_folder):
        self.data = {}
        self.labels = {}
        print(f"📥 Loading DEAP subjects from: {data_folder}")

        for fname in sorted(os.listdir(data_folder)):
            if not fname.endswith(".mat"):
                continue

            subject = fname.split(".")[0]   # "s01"
            path = os.path.join(data_folder, fname)

            mat = sio.loadmat(path, simplify_cells=True)
            raw_data = mat["data"]        # shape (40,40,8064)
            raw_labels = mat["labels"]    # shape (40,4)

            # Extract arousal labels and binarize
            arousal = raw_labels[:, 1]
            bin_labels = (arousal >= 5).astype(int)

            subject_samples = []
            subject_labels = []

            for i in range(40):
                trial = raw_data[i][:32]   # (32, 8064)

                # Normalize each channel
                for c in range(32):
                    ch = trial[c]
                    trial[c] = (ch - ch.mean()) / (ch.std() + 1e-6)

                # Reshape (32 × 8064) -> (1 × 32 × 252)
                reshaped = []
                for c in range(32):
                    ch = trial[c].reshape(252, 32)
                    reshaped.append(ch)

                reshaped = np.stack(reshaped)[:, :, 0]  # (32, 252)
                tensor = torch.tensor(reshaped, dtype=torch.float32).unsqueeze(0)

                subject_samples.append(tensor)
                subject_labels.append(int(bin_labels[i]))

            self.data[subject] = subject_samples
            self.labels[subject] = subject_labels

        print(f"✅ Loaded {len(self.data)} subjects.")
