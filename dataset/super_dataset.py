import torch
from torch.utils.data import Dataset


class SuperDataset(Dataset):
    """
    Hybrid dataset merging:
        RAW EEG:        (32,59,128)
        MULTIBAND EEG:  (32,W,4,128)
    """

    def __init__(self, subjects, raw_data, mb_data, labels, device):
        self.samples = []
        self.device = device

        for sid in subjects:
            r_trials = raw_data[sid]
            m_trials = mb_data[sid]
            labs = labels[sid]

            for i in range(len(r_trials)):
                self.samples.append((r_trials[i], m_trials[i], labs[i]))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        raw_trial, mb_trial, label = self.samples[idx]

        # RAW EEG: shape (32,59,128)
        raw = torch.tensor(raw_trial, dtype=torch.float32).unsqueeze(0)
        # → (1,32,59,128)

        # MULTIBAND EEG: shape (32,W,4,128)
        mb = torch.tensor(mb_trial, dtype=torch.float32).unsqueeze(0)
        # → (1,32,W,4,128)

        y = torch.tensor(label, dtype=torch.float32)

        return raw, mb, y
