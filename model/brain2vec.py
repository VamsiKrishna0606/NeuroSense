import torch
import torch.nn as nn

# ============================================
# Generic Multi-Head Attention Block
# ============================================
class MHA_Block(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        self.attn = nn.MultiheadAttention(embed_dim, num_heads, batch_first=True)
        self.norm = nn.LayerNorm(embed_dim)

    def forward(self, x):
        attn_out, _ = self.attn(x, x, x)
        return self.norm(attn_out + x)  # Residual
        

# ============================================
# Spatial Attention Block (Learnable importance of EEG channels)
# ============================================
class SpatialAttention(nn.Module):
    def __init__(self, channels, embed_dim):
        super().__init__()
        self.score = nn.Sequential(
            nn.Linear(embed_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1)    # output = importance weight for each channel
        )
        self.softmax = nn.Softmax(dim=1)  # across channels

    def forward(self, x):
        # x: (B, 32, 128)
        weights = self.score(x)           # (B, 32, 1)
        weights = self.softmax(weights)   # normalized across channels

        return x * weights                # weighted features
        

# ============================================
# FINAL MODEL
# ============================================
class Brain2Vec(nn.Module):
    def __init__(self):
        super().__init__()

        # ------------------------------------------------
        # 1) LINEAR EMBEDDING PER CHANNEL
        # ------------------------------------------------
        self.channel_embed = nn.Linear(252, 128)   # (252 → 128)

        # ------------------------------------------------
        # 2) Channel Attention (Done previously)
        # ------------------------------------------------
        self.channel_mha = MHA_Block(embed_dim=128, num_heads=4)

        # ------------------------------------------------
        # 3) Temporal Attention (Done previously)
        # ------------------------------------------------
        self.temporal_mha = MHA_Block(embed_dim=128, num_heads=4)

        # ------------------------------------------------
        # 4) NEW SPATIAL ATTENTION (BEST PLACE = BEFORE LSTM)
        # ------------------------------------------------
        self.spatial_att = SpatialAttention(channels=32, embed_dim=128)

        # ------------------------------------------------
        # 5) BiLSTM for Sequence Modeling
        # ------------------------------------------------
        self.lstm = nn.LSTM(
            input_size=128,
            hidden_size=64,
            num_layers=1,
            batch_first=True,
            bidirectional=True
        )

        # ------------------------------------------------
        # 6) Classification Head
        # ------------------------------------------------
        self.fc = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.25),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        # x: (B, 1, 32, 252)
        x = x.squeeze(1)                    # (B, 32, 252)

        x = self.channel_embed(x)           # (B, 32, 128)

        x = self.channel_mha(x)             # Channel Attention
        x = self.temporal_mha(x)            # Temporal Attention

        x = self.spatial_att(x)             # ★ Spatial Attention Before LSTM

        lstm_out, _ = self.lstm(x)          # (B, 32, 128)

        last = lstm_out[:, -1, :]           # last timestep (B,128)

        return self.fc(last)                # (B,1)
