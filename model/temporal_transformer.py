import torch
import torch.nn as nn


class TemporalTransformer(nn.Module):
    """
    Multi-layer temporal transformer for both raw & multiband branches.

    Input:  (B, T, 256)
    Output: (B, T, 256)
    """

    def __init__(self, d_model=256, num_layers=4, nhead=4, ff_dim=512, dropout=0.1):
        super().__init__()

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=ff_dim,
            dropout=dropout,
            batch_first=True,
            norm_first=True
        )

        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

    def forward(self, x):
        # x: (B,T,256)
        return self.encoder(x)
