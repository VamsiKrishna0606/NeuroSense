import os
import scipy.io as sio
import torch
import numpy as np
from torch.utils.data import Dataset

class DEAPDataset(Dataset):
    def __init__(self, data_folder):

        self.samples = []
        self.labels = []

        print(f"📥 Loading DEAP .mat files from: {data_folder}")

        for file in sorted(os.listdir(data_folder)):
            if not file.endswith(".mat"):
                continue

            path = os.path.join(data_folder, file)
            mat = sio.loadmat(path, simplify_cells=True)

            data = mat["data"]        # (40, 40, 8064)
            labels = mat["labels"]    # (40,4)

            arousal = labels[:, 1]
            bin_labels = (arousal >= 5).astype(int)

            for i in range(40):

                # take first 32 EEG channels → (32, 8064)
                trial = data[i][:32]       # shape (32, 8064)

                # Normalize each channel
                for c in range(32):
                    ch = trial[c]
                    ch = (ch - ch.mean()) / (ch.std() + 1e-6)
                    trial[c] = ch

                # Reshape EACH CHANNEL → (252, 32)
                reshaped = []
                for c in range(32):
                    ch = trial[c]              # (8064,)
                    ch = ch.reshape(252, 32)   # (252, 32)
                    reshaped.append(ch)

                # Stack channels -> (32, 252, 32)
                reshaped = np.stack(reshaped)   # shape (32,252,32)

                # Now collapse middle dimension for CNN:
                # Final shape we want: (1, 32, 252)
                # So we take ONLY time dimension (252)
                reshaped = reshaped[:, :, 0]    # take first slice → (32,252)

                tensor = torch.tensor(reshaped, dtype=torch.float32).unsqueeze(0)

                self.samples.append(tensor)
                self.labels.append(int(bin_labels[i]))

        print(f"✅ Loaded {len(self.samples)} samples")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx], torch.tensor(self.labels[idx]).long()
