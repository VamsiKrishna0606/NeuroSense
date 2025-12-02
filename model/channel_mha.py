import torch
import torch.nn as nn


class ChannelMHA(nn.Module):
    """
    Multi-head attention across the 32 EEG channels.

    Input:  (B, 32, 256)
    Output: (B, 32, 256)
    """
    def __init__(self, embed_dim=256, num_heads=6):
        super().__init__()
        self.norm = nn.LayerNorm(embed_dim)
        self.mha = nn.MultiheadAttention(
            embed_dim=embed_dim,
            num_heads=num_heads,
            batch_first=True
        )

    def forward(self, x):
        h = self.norm(x)
        out, _ = self.mha(h, h, h)
        return x + out
