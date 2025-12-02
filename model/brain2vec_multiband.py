import torch
import torch.nn as nn


class BandCNN(nn.Module):
    """
    Extract features from each band window (4 bands, 128 samples)
    Input: (B, 4, 128)
    Output: (B, 128)
    """
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv1d(4, 32, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.Conv1d(32, 64, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1)
        )
        self.fc = nn.Linear(64, 128)

    def forward(self, x):  # x: (B,4,128)
        h = self.net(x)     # (B,64,1)
        h = h.squeeze(-1)   # (B,64)
        return self.fc(h)   # (B,128)


class MHA_Block(nn.Module):
    def __init__(self, embed_dim=128, num_heads=4):
        super().__init__()
        self.norm = nn.LayerNorm(embed_dim)
        self.mha = nn.MultiheadAttention(embed_dim, num_heads, batch_first=True)

    def forward(self, x):
        h = self.norm(x)
        out, _ = self.mha(h, h, h)
        return x + out


class Brain2Vec_MultiBand(nn.Module):
    """
    Input: (B, 1, 32, 60, 4, 128)
    """
    def __init__(self):
        super().__init__()

        # CNN for band extraction
        self.band_cnn = BandCNN()

        # Temporal transformer
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=128,
            nhead=4,
            dim_feedforward=256,
            dropout=0.1,
            batch_first=True,
            norm_first=True
        )
        self.temp_transformer = nn.TransformerEncoder(encoder_layer, num_layers=1)

        # Channel-level attention
        self.channel_mha = MHA_Block(embed_dim=128, num_heads=4)

        # BiLSTM
        self.lstm = nn.LSTM(
            input_size=128,
            hidden_size=64,
            num_layers=2,
            batch_first=True,
            bidirectional=True,
            dropout=0.1
        )

        # Fusion
        self.fusion = nn.Sequential(
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.LayerNorm(128)
        )

        # Final classifier
        self.classifier = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        # x: (B, 1, 32, 60, 4, 128)
        x = x.squeeze(1)  # (B, 32, 60, 4, 128)
        B, C, W, BANDS, S = x.shape

        # ===== Step 1: Band CNN on each window =====
        x = x.view(B * C * W, BANDS, S)   # (B*C*W, 4,128)
        x = self.band_cnn(x)              # (B*C*W,128)
        x = x.view(B, C, W, 128)          # (B,32,60,128)

        # ===== Step 2: Temporal transformer =====
        x = x.view(B * C, W, 128)         # (B*C,60,128)
        x = self.temp_transformer(x)      # (B*C,60,128)
        x = x.view(B, C, W, 128)

        # ===== ⭐ FIX: Pool over windows before channel-MHA =====
        x = x.mean(dim=2)                 # (B,32,128)

        # ===== Step 3: Channel attention (MHA) =====
        x = self.channel_mha(x)           # (B,32,128)

        # ===== Step 4: BiLSTM =====
        lstm_out, _ = self.lstm(x)        # (B,32,128)
        final = lstm_out[:, -1, :]        # (B,128)

        # ===== Step 5: Fusion + Classifier =====
        final = self.fusion(final)
        out = self.classifier(final)

        return out
