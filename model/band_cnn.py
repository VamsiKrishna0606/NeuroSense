import torch
import torch.nn as nn


class BandCNN(nn.Module):
    """
    Input:  (B, 4, 128)
    Output: (B, 256)
    Spectral CNN for multi-band signals.
    """
    def __init__(self):
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv1d(4, 64, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.Conv1d(64, 128, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.Conv1d(128, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1)
        )

        self.fc = nn.Linear(128, 256)

    def forward(self, x):
        # x: (B,4,128)
        h = self.features(x)       # (B,128,1)
        h = h.squeeze(-1)          # (B,128)
        return self.fc(h)          # (B,256)
