import torch
import torch.nn as nn


class SpatialAttention(nn.Module):
    """
    Spatial attention across EEG channels or feature maps.

    Input:  (B, C, F)
    Output: (B, C, F) with attention applied
    """
    def __init__(self, channels=32, embed_dim=256):
        super().__init__()

        self.query = nn.Linear(embed_dim, embed_dim)
        self.key   = nn.Linear(embed_dim, embed_dim)
        self.value = nn.Linear(embed_dim, embed_dim)

        self.softmax = nn.Softmax(dim=-1)
        self.proj = nn.Linear(embed_dim, embed_dim)

    def forward(self, x):
        # x: (B,C,256)
        Q = self.query(x)     # (B,C,256)
        K = self.key(x)       # (B,C,256)
        V = self.value(x)     # (B,C,256)

        att = torch.matmul(Q, K.transpose(-1, -2)) / (256 ** 0.5)
        att = self.softmax(att)         # (B,C,C)

        out = torch.matmul(att, V)      # (B,C,256)
        out = self.proj(out)

        return x + out
