import torch
import torch.nn as nn


class BiLSTMBlock(nn.Module):
    """
    Input:  (B, T, 256)
    Output: (B, 512)
    """

    def __init__(self, input_dim=256, hidden_dim=256, num_layers=2, dropout=0.1):
        super().__init__()

        self.lstm = nn.LSTM(
            input_dim,
            hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=dropout
        )

    def forward(self, x):
        # x: (B,T,256)
        out, _ = self.lstm(x)  # (B,T,512)
        return out[:, -1, :]   # last timestep (B,512)
