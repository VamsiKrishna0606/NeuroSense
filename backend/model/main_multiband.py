import torch
import torch.nn as nn


class BandCNN(nn.Module):
    """
    Extract features from each frequency band
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

    def forward(self, x):
        h = self.net(x)        # (B,64,1)
        h = h.squeeze(-1)      # (B,64)
        return self.fc(h)      # (B,128)


class MHA_Block(nn.Module):
    """
    Channel-level Multi-Head Attention
    """
    def __init__(self, embed_dim=128, num_heads=4):
        super().__init__()
        self.norm = nn.LayerNorm(embed_dim)
        self.mha = nn.MultiheadAttention(
            embed_dim, num_heads, batch_first=True
        )

    def forward(self, x):
        h = self.norm(x)
        out, _ = self.mha(h, h, h)
        return x + out


class Brain2Vec_MultiBand(nn.Module):
    """
    Brain2Vec Multiband EEG Model
    Expected Input Shape:
    (B, 1, 32, 60, 4, 128)
    """
    def __init__(self):
        super().__init__()

        # Band-wise CNN
        self.band_cnn = BandCNN()

        # Temporal Transformer
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=128,
            nhead=4,
            dim_feedforward=256,
            dropout=0.1,
            batch_first=True,
            norm_first=True
        )
        self.temp_transformer = nn.TransformerEncoder(
            encoder_layer, num_layers=1
        )

        # Channel Attention
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

        # Fusion Layer
        self.fusion = nn.Sequential(
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.LayerNorm(128)
        )

        # Final Classifier
        self.classifier = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        """
        x: (B, 1, 32, 60, 4, 128)
        """
        x = x.squeeze(1)              # (B,32,60,4,128)
        B, C, W, BANDS, S = x.shape

        # ----- Band CNN -----
        #x = x.view(B * C * W, BANDS, S)   # (B*C*W,4,128)
        x = x.reshape(B * C * W, BANDS, S)
        x = self.band_cnn(x)              # (B*C*W,128)
        x = x.view(B, C, W, 128)          # (B,32,60,128)

        # ----- Temporal Transformer -----
        x = x.view(B * C, W, 128)         # (B*C,60,128)
        x = self.temp_transformer(x)
        x = x.view(B, C, W, 128)

        # ----- Pool over time windows -----
        x = x.mean(dim=2)                 # (B,32,128)

        # ----- Channel Attention -----
        x = self.channel_mha(x)           # (B,32,128)

        # ----- BiLSTM -----
        lstm_out, _ = self.lstm(x)
        final = lstm_out[:, -1, :]        # (B,128)

        # ----- Fusion + Classification -----
        final = self.fusion(final)
        out = self.classifier(final)      # (B,1)

        return out
