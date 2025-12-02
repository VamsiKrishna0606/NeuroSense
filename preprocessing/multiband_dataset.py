import torch
from torch.utils.data import Dataset

class MultibandDataset(Dataset):
    def __init__(self, subjects, data, labels, device):
        self.samples = []
        self.device = device

        for subj in subjects:
            trials = data[subj]
            labs = labels[subj]

            for i in range(len(trials)):
                self.samples.append((trials[i], labs[i]))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        trial, label = self.samples[idx]

        # trial shape: (32,60,4,128)
        X = torch.tensor(trial, dtype=torch.float32).unsqueeze(0)  # (1,32,60,4,128)
        y = torch.tensor(label, dtype=torch.float32)

        return X, y
