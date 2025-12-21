import torch
import numpy as np
import scipy.io as sio
from model.main_multiband import Brain2Vec_MultiBand


DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = Brain2Vec_MultiBand().to(DEVICE)
model.load_state_dict(torch.load("model/multiband_all_subjects.pth", map_location=DEVICE))
model.eval()


def preprocess(file_path):
    mat = sio.loadmat(file_path)
    raw = mat["data"]            # (40,40,8064)

    eeg = raw[0, :32, :]         # one trial → (32,8064)

    eeg = eeg[:, :60*128]        # trim
    eeg = eeg.reshape(32, 60, 128)

    eeg = np.stack([eeg]*4, axis=3)
    eeg = np.transpose(eeg, (0,1,3,2))

    x = torch.tensor(eeg).unsqueeze(0).unsqueeze(0).float()
    return x.to(DEVICE)


def run_prediction(file_path):
    x = preprocess(file_path)

    with torch.no_grad():
        logits = model(x)
        prob = torch.sigmoid(logits).item()

    return {
        "valence": "HIGH" if prob >= 0.5 else "LOW",
        "confidence": round(prob, 4),
        "interpretation": "Positive emotional engagement detected"
        if prob >= 0.5 else
        "Low emotional arousal detected"
    }
