import torch
import torch.nn as nn


# ------------------------------------------------------------
# PreNorm MHA Block
# ------------------------------------------------------------
class MHA_Block(nn.Module):
    def __init__(self, dim, heads):
        super().__init__()
        self.norm = nn.LayerNorm(dim)
        self.attn = nn.MultiheadAttention(
            embed_dim=dim,
            num_heads=heads,
            batch_first=True
        )

    def forward(self, x):
        h = self.norm(x)
        out, _ = self.attn(h, h, h)
        return x + out


# ------------------------------------------------------------
# Brain2Vec C3 – Transformer Temporal Encoder Version
# ------------------------------------------------------------
class Brain2Vec(nn.Module):
    def __init__(self):
        super().__init__()

        self.embed_dim = 128

        # Project each window from 128 → 128
        self.window_embed = nn.Sequential(
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.LayerNorm(128)
        )

        # Transformer Temporal Encoder
        self.temporal_mha = MHA_Block(dim=128, heads=4)
        self.temporal_ff = nn.Sequential(
            nn.LayerNorm(128),
            nn.Linear(128, 128),
            nn.ReLU()
        )

        # Channel Fusion using BiLSTM
        self.lstm = nn.LSTM(
            input_size=128,
            hidden_size=64,
            bidirectional=True,
            batch_first=True
        )

        # Final Classifier
        self.classifier = nn.Sequential(
            nn.LayerNorm(128),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        # x: (B, 32, W, 128)

        B, C, W, F = x.shape

        # Embed each 128-dim window
        x = self.window_embed(x)          # (B, 32, W, 128)

        # Flatten channels → process temporal windows individually
        x = x.view(B * C, W, F)

        # Transformer temporal encoder
        x = self.temporal_mha(x)
        x = self.temporal_ff(x)

        # Take final window output
        x = x[:, -1, :]                   # (B*C, 128)

        # Reshape back to channels
        x = x.view(B, C, 128)             # (B, 32, 128)

        # Channel BiLSTM
        lstm_out, _ = self.lstm(x)        # (B, 32, 128)
        fused = lstm_out[:, -1, :]        # (B, 128)

        return self.classifier(fused)     # (B, 1)
