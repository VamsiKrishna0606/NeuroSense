import torch
import torch.nn as nn


# ============================================================
# Generic PreNorm Multi-Head Attention Block
# ============================================================
class MHA_Block(nn.Module):
    def __init__(self, embed_dim, num_heads, dropout=0.1):
        super().__init__()
        self.norm = nn.LayerNorm(embed_dim)
        self.attn = nn.MultiheadAttention(
            embed_dim,
            num_heads,
            dropout=dropout,
            batch_first=True
        )
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        """
        x: (B, 32, 128) for channel attention
        """
        h = self.norm(x)
        attn_out, _ = self.attn(h, h, h)
        return x + self.dropout(attn_out)  # Residual
        

# ============================================================
# Spatial Attention (learnable weights for each EEG channel)
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
        x: (B, 32, 128)
        """
        w = self.score(x)        # (B, 32, 1)
        w = self.softmax(w)      # normalize importance across channels
        return x * w             # weighted EEG channel features
        

# ============================================================
# C3 Transformer Temporal Encoder (NEW)
# ============================================================
class TransformerTemporalEncoder(nn.Module):
    def __init__(self, embed_dim=128, num_heads=4, ff_dim=256, dropout=0.1):
        super().__init__()

        layer = nn.TransformerEncoderLayer(
            d_model=embed_dim,
            nhead=num_heads,
            dim_feedforward=ff_dim,
            dropout=dropout,
            batch_first=True,
            activation="gelu",
            norm_first=True    # ⚡️ Critical for stability
        )

        self.encoder = nn.TransformerEncoder(
            layer,
            num_layers=1        # C3 uses 1–2 layers; 1 is perfect for DEAP
        )

    def forward(self, x):
        """
        x: (B, 32, 128)
        """
        return self.encoder(x)
        

# ============================================================
# FINAL MODEL — Brain2Vec C3 (Channel + Spatial + Transformer + BiLSTM)
# ============================================================
class Brain2Vec(nn.Module):
    def __init__(self):
        super().__init__()

        self.embed_dim = 128

        # -----------------------------------------------------
        # 1) Channel Embedding
        # -----------------------------------------------------
        self.channel_embed = nn.Sequential(
            nn.LayerNorm(128),
            nn.Linear(128, 128),
            nn.ReLU(),
        )

        # -----------------------------------------------------
        # 2) Channel-Level MHA
        # -----------------------------------------------------
        self.channel_mha = MHA_Block(embed_dim=128, num_heads=4)

        # -----------------------------------------------------
        # 3) TEMPORAL TRANSFORMER (C3 UPGRADE)
        # -----------------------------------------------------
        self.temp_transformer = TransformerTemporalEncoder(
            embed_dim=128,
            num_heads=4,
            ff_dim=256,
            dropout=0.1
        )

        # -----------------------------------------------------
        # 4) Spatial Attention
        # -----------------------------------------------------
        self.spatial_att = SpatialAttention(channels=32, embed_dim=128)

        # -----------------------------------------------------
        # 5) BiLSTM Encoder
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
        # 6) Fusion Layer
        # -----------------------------------------------------
        self.fusion = nn.Sequential(
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.LayerNorm(128)
        )

        # -----------------------------------------------------
        # 7) Final Classifier Head
        # -----------------------------------------------------
        self.classifier = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        # x: (B, 1, 32, 63, 128)
        x = x.squeeze(1)   # (B, 32, 63, 128)

        # Reduce temporal dimension: mean over 63 frames
        x = x.mean(dim=2)         # (B, 32, 128)

        # Channel embedding
        x = self.channel_embed(x) # (B, 32, 128)

        # Channel MHA
        x = self.channel_mha(x)   # (B, 32, 128)

        # 🔥 C3 Temporal Transformer
        x = self.temp_transformer(x)  # (B, 32, 128)

        # Spatial attention
        x = self.spatial_att(x)       # (B, 32, 128)

        # BiLSTM encoding
        lstm_out, _ = self.lstm(x)    # (B, 32, 128)
        fused = lstm_out[:, -1, :]    # Take last time step → (B, 128)

        # Fusion + classifier
        fused = self.fusion(fused)    # (B, 128)
        out = self.classifier(fused)  # (B, 1)

        return out
