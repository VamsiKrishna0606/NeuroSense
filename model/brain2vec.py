import torch
import torch.nn as nn

# ------------------------------
# Multi-Head Attention Block
# ------------------------------
class MHA_Block(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        self.attn = nn.MultiheadAttention(embed_dim, num_heads, batch_first=True)
        self.norm = nn.LayerNorm(embed_dim)

    def forward(self, x):
        attn_out, _ = self.attn(x, x, x)
        return self.norm(attn_out + x)   # residual connection


class Brain2Vec(nn.Module):
    def __init__(self):
        super().__init__()

        # Input shape: (B, 1, 32, 252)
        # Embed each channel's 252 samples → 128-dim vector
        self.channel_embed = nn.Linear(252, 128)

        # ------------------------------------------------
        # STEP-A: Channel-wise Attention (ALREADY DONE)
        # ------------------------------------------------
        self.channel_mha = MHA_Block(embed_dim=128, num_heads=4)

        # ------------------------------------------------
        # STEP-B: Temporal Attention (NEW)
        # ------------------------------------------------
        self.temporal_mha = MHA_Block(embed_dim=128, num_heads=4)

        # BiLSTM to capture sequential features
        self.lstm = nn.LSTM(
            input_size=128,
            hidden_size=64,
            num_layers=1,
            batch_first=True,
            bidirectional=True
        )

        # Final classifier
        self.fc = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.25),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        # x: (B, 1, 32, 252)
        x = x.squeeze(1)                 # (B, 32, 252)

        # Channel embedding
        x = self.channel_embed(x)        # (B, 32, 128)

        # Channel attention
        x = self.channel_mha(x)          # (B, 32, 128)

        # Temporal attention
        x = self.temporal_mha(x)         # (B, 32, 128)

        # BiLSTM
        lstm_out, _ = self.lstm(x)       # (B, 32, 128)

        # Last hidden state
        last = lstm_out[:, -1, :]        # (B, 128)

        # Final prediction
        out = self.fc(last)              # (B, 1)
        return out
