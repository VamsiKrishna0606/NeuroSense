import torch
import torch.nn as nn
import torch.nn.functional as F


class AttentionBlock(nn.Module):
    def __init__(self, hidden_dim):
        super().__init__()
        self.att = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        w = self.att(x)               # (B, T, 1)
        w = F.softmax(w, dim=1)
        ctx = torch.sum(w * x, dim=1)
        return ctx


class Brain2Vec(nn.Module):
    def __init__(self, num_classes=1):  # BCE → 1 output
        super().__init__()

        # Input shape: (1, 32, 252)
        self.cnn = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(16, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )

        # CNN output = (64, 4, 31)
        self.feature_dim = 64 * 4    # 256
        self.seq_len = 31

        self.lstm = nn.LSTM(
            input_size=self.feature_dim,
            hidden_size=128,
            batch_first=True
        )

        self.att = AttentionBlock(128)

        self.fc = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        cnn_out = self.cnn(x)             # (B,64,4,31)
        B, C, H, T = cnn_out.shape

        lstm_in = cnn_out.permute(0, 3, 1, 2).reshape(
            B, T, C * H
        )  # (B,31,256)

        lstm_out, _ = self.lstm(lstm_in)
        ctx = self.att(lstm_out)
        out = self.fc(ctx)

        return out  # (B,1)
