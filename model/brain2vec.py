import torch
import torch.nn as nn


# ============================================================
# Generic PreNorm Multi-Head Attention Block
# ============================================================
class MHA_Block(nn.Module):
    def __init__(self, embed_dim, num_heads, dropout=0.1):
        super().__init__()
        self.norm = nn.LayerNorm(embed_dim)
        self.attn = nn.MultiheadAttention(embed_dim, num_heads, dropout=dropout, batch_first=True)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        """
        x: (B, T, C) for temporal or (B, Channels, C) for channel attention
        """
        h = self.norm(x)
        attn_out, _ = self.attn(h, h, h)
        return x + self.dropout(attn_out)    # Residual
        

# ============================================================
# Spatial Attention (learnable weights for channels)
# ============================================================
class SpatialAttention(nn.Module):
    def __init__(self, channels, embed_dim):
        super().__init__()
        self.score = nn.Sequential(
            nn.Linear(embed_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        """
        x: (B, 32, C)
        Returns: (B, 32, C) weighted by importance
        """
        w = self.score(x)            # (B, 32, 1)
        w = self.softmax(w)          # normalize across channels
        return x * w                 # weighted channel features
        

# ============================================================
# UPGRADED FINAL MODEL — Brain2Vec-Upgrade C2
# ============================================================
class Brain2Vec(nn.Module):
    def __init__(self):
        super().__init__()

        # -----------------------------------------------------
        # INPUT ASSUMED SHAPE:
        # (B, 1, 32, 63, 128)
        # -----------------------------------------------------

        self.embed_dim = 128

        # -----------------------------------------------------
        # 1) Channel Embedding
        # Each channel → 63×128 flattened → 8064 → 128 vector
        # -----------------------------------------------------
        self.channel_embed = nn.Sequential(
            nn.LayerNorm(128),
            nn.Linear(128, 128),
            nn.ReLU(),
        )

        # -----------------------------------------------------
        # 2) Channel MHA (across 32 channels)
        # -----------------------------------------------------
        self.channel_mha = MHA_Block(embed_dim=128, num_heads=4)

        # -----------------------------------------------------
        # 3) Temporal MHA (across 63 time steps)
        # -----------------------------------------------------
        self.temp_mha = MHA_Block(embed_dim=128, num_heads=4)

        # -----------------------------------------------------
        # 4) Spatial Attention (weights for each channel)
        # -----------------------------------------------------
        self.spatial_att = SpatialAttention(channels=32, embed_dim=128)

        # -----------------------------------------------------
        # 5) BiLSTM Encoder (C2 Upgrade)
        # -----------------------------------------------------
        self.lstm = nn.LSTM(
            input_size=128,
            hidden_size=64,
            num_layers=2,
            dropout=0.1,
            batch_first=True,
            bidirectional=True
        )

        # -----------------------------------------------------
        # 6) Feature Fusion
        # -----------------------------------------------------
        self.fusion = nn.Sequential(
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.LayerNorm(128)
        )

        # -----------------------------------------------------
        # 7) Classification Head
        # -----------------------------------------------------
        self.classifier = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        # x: (B, 1, 32, 63, 128)
        x = x.squeeze(1)        # (B, 32, 63, 128)

        B, C, T, F = x.shape

        # -----------------------------------------------------
        # 1) PER-CHANNEL TEMPORAL AVERAGE → reduces dimension
        # -----------------------------------------------------
        x = x.mean(dim=2)       # (B, 32, 128)

        # -----------------------------------------------------
        # 2) Channel Embedding
        # -----------------------------------------------------
        x = self.channel_embed(x)   # (B, 32, 128)

        # -----------------------------------------------------
        # 3) Channel MHA (across 32 channels)
        # -----------------------------------------------------
        x = self.channel_mha(x)     # (B, 32, 128)

        # -----------------------------------------------------
        # 4) Temporal MHA (reshape to temporal sequence)
        # -----------------------------------------------------
        x_temp = x.permute(0, 2, 1)  # (B, 128, 32)
        x_temp = self.temp_mha(x_temp)
        x = x_temp.permute(0, 2, 1)  # back to (B, 32, 128)

        # -----------------------------------------------------
        # 5) Spatial Attention
        # -----------------------------------------------------
        x = self.spatial_att(x)      # (B, 32, 128)

        # -----------------------------------------------------
        # 6) LSTM Encoder (C2 implementation)
        # -----------------------------------------------------
        lstm_out, _ = self.lstm(x)   # (B, 32, 128)
        fused = lstm_out[:, -1, :]   # (B, 128)

        # -----------------------------------------------------
        # 7) Fusion + Classifier
        # -----------------------------------------------------
        fused = self.fusion(fused)   # (B, 128)
        out = self.classifier(fused) # (B, 1)

        return out
