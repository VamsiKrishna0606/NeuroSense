import torch
import torch.nn as nn

from model.band_cnn import BandCNN
from model.temporal_transformer import TemporalTransformer
from model.spatial_attention import SpatialAttention
from model.channel_mha import ChannelMHA
from model.bilstm_block import BiLSTMBlock


class ETLAFSuperModel(nn.Module):
    """
    E T L A F  SUPERMODEL
    -------------------------------------
    Extract (Raw + Multiband)
    Transform (Temporal Transformers)
    Learn (BiLSTM)
    Attend (Spatial + Channel)
    Fuse (Hybrid Fusion)
    -------------------------------------
    Supports RAW:       (B,1,32,59,128)
    Supports MULTIBAND: (B,1,32,W,4,128)
    """

    def __init__(
        self,
        raw_embed_dim=256,
        mb_embed_dim=256,
        fusion_dim=256
    ):
        super().__init__()

        # -------------------------------------------------------
        # RAW BRANCH
        # -------------------------------------------------------
        self.raw_linear = nn.Linear(128, raw_embed_dim)

        self.raw_transformer = TemporalTransformer(
            d_model=raw_embed_dim,
            num_layers=4,
            nhead=4,
            ff_dim=512,
            dropout=0.1
        )

        self.raw_spatial_att = SpatialAttention(
            channels=32,
            embed_dim=raw_embed_dim
        )

        self.raw_lstm = BiLSTMBlock(
            input_dim=raw_embed_dim,
            hidden_dim=256,
            num_layers=2,
            dropout=0.1
        )

        # -------------------------------------------------------
        # MULTIBAND BRANCH
        # -------------------------------------------------------
        self.band_cnn = BandCNN()   # output = 256 dim

        self.mb_transformer = TemporalTransformer(
            d_model=mb_embed_dim,
            num_layers=4,
            nhead=4,
            ff_dim=512,
            dropout=0.1
        )

        self.mb_channel_att = ChannelMHA(
            embed_dim=mb_embed_dim,
            num_heads=4
        )

        self.mb_lstm = BiLSTMBlock(
            input_dim=mb_embed_dim,
            hidden_dim=256,
            num_layers=2,
            dropout=0.1
        )

        # -------------------------------------------------------
        # FUSION LAYER
        # -------------------------------------------------------
        self.fusion = nn.Sequential(
            nn.Linear(512 + 512, fusion_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.LayerNorm(fusion_dim),
            nn.Linear(fusion_dim, fusion_dim),
            nn.ReLU(),
            nn.Dropout(0.2)
        )

        # -------------------------------------------------------
        # CLASSIFIER
        # -------------------------------------------------------
        self.classifier = nn.Sequential(
            nn.Linear(fusion_dim, 128),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Linear(64, 1)
        )

    # ===========================================================
    # FORWARD PASS
    # ===========================================================
    def forward(self, raw, mb):
        """
        raw: (B,1,32,59,128)
        mb:  (B,1,32,W,4,128)
        """
        B = raw.size(0)

        # -------------------------------
        # RAW BRANCH
        # -------------------------------
        raw = raw.squeeze(1)  # (B,32,59,128)

        raw = self.raw_linear(raw)  # (B,32,59,256)

        raw_t = raw.view(B * 32, raw.size(2), raw.size(3))
        raw_t = self.raw_transformer(raw_t)
        raw_t = raw_t.view(B, 32, raw.size(2), raw.size(3))

        raw_t2 = self.raw_spatial_att(raw_t.mean(dim=2))  # (B,32,256)

        raw_feat = self.raw_lstm(raw_t2)  # (B,512)

        # -------------------------------
        # MULTIBAND BRANCH
        # -------------------------------
        mb = mb.squeeze(1)
        B, C, W, _, S = mb.shape

        mb_flat = mb.view(B * C * W, 4, 128)
        mb_embed = self.band_cnn(mb_flat)   # (B*C*W,256)

        mb_embed = mb_embed.view(B, C, W, 256)

        mb_t = mb_embed.view(B * C, W, 256)
        mb_t = self.mb_transformer(mb_t)
        mb_t = mb_t.view(B, C, W, 256)

        mb_att = self.mb_channel_att(mb_t.mean(dim=2))

        mb_feat = self.mb_lstm(mb_att)  # (B,512)

        # -------------------------------
        # FUSION
        # -------------------------------
        fused = torch.cat([raw_feat, mb_feat], dim=1)

        fused = self.fusion(fused)

        # -------------------------------
        # CLASSIFIER
        # -------------------------------
        out = self.classifier(fused)

        return out
