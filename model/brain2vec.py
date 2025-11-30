import torch
import torch.nn as nn


class Brain2Vec(nn.Module):
    def __init__(self):
        super(Brain2Vec, self).__init__()

        # --------------------------
        # 1. CNN Feature Extractor
        # --------------------------
        self.cnn = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=(3, 3), padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),

            nn.Conv2d(32, 64, kernel_size=(3, 3), padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),

            nn.MaxPool2d(kernel_size=(2, 2))  # (32,252) → (16,126)
        )

        # --------------------------
        # 2. Prepare for Attention
        # --------------------------
        self.embedding_dim = 64 * 16   # = 1024
        self.seq_len = 126

        self.linear_proj = nn.Linear(1024, 128)

        # --------------------------
        # 3. Multi-Head Self Attention
        # --------------------------
        self.mha = nn.MultiheadAttention(
            embed_dim=128,
            num_heads=4,
            dropout=0.1,
            batch_first=True
        )

        # --------------------------
        # 4. Classification Head
        # --------------------------
        self.fc = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        # x: (B, 1, 32, 252)

        x = self.cnn(x)  # (B,64,16,126)

        B, C, H, T = x.shape

        x = x.permute(0, 3, 1, 2)    # (B,T,C,H)
        x = x.reshape(B, T, C * H)   # (B,T,1024)

        x = self.linear_proj(x)       # (B,T,128)

        attn_out, _ = self.mha(x, x, x)

        pooled = attn_out.mean(dim=1)

        return self.fc(pooled)
