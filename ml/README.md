# NeuroSense – EEG Emotion Recognition (DEAP Dataset)

## Step 1 Completed — Full Model Recreation from Research Paper

This repository contains a clean reconstruction of the CNN → LSTM → Attention model described in the research paper. This implementation serves as the baseline for upcoming enhancements such as continuous regression, Brain2Vec embeddings, and transformer-based upgrades.

---

## Project Structure

NeuroSense/
│
├── main.py
│
├── preprocessing/
│   ├── deap_preprocess.py
│   ├── __init__.py
│
├── model/
│   ├── brain2vec.py
│   ├── __init__.py
│
├── training/
│   ├── train.py
│   ├── __init__.py
│
├── evaluation/
│   ├── evaluate.py
│   ├── __init__.py
│
├── utils/
│   ├── plot_utils.py
│   ├── __init__.py
│
├── data/        (ignored)
│
├── requirements.txt
├── README.md
└── .gitignore

---

## Current Achievements

- Successfully recreated the full model architecture from the research paper.
- Preprocessing for DEAP EEG dataset: 32 channels → 8064 samples → reshaped to (32, 252).
- CNN extracts spatial EEG features.
- LSTM captures temporal patterns.
- Attention layer highlights important time segments.
- Final FC layer produces binary emotion predictions.
- Uses balanced sampling + BCEWithLogitsLoss.
- Achieved approximately:
  - 98% accuracy
  - 0.995 AUC

---

## Dataset (DEAP)

Download DEAP dataset from:

http://www.eecs.qmul.ac.uk/mmv/datasets/deap/

Place all `.mat` files in:

NeuroSense/data/deap/

The dataset is large (~3GB) and is therefore excluded via `.gitignore`.

---

## Running the Project

### Install Dependencies:
pip install -r requirements.txt

### Run Training:
python main.py

This automatically:
- Loads DEAP dataset
- Preprocesses each trial
- Trains CNN → LSTM → Attention model
- Saves best model checkpoint

---

## Model Summary

- CNN: Spatial feature extraction across 32 EEG channels.
- LSTM: Temporal modeling across 252 time steps.
- Attention: Assigns importance weights to temporal segments.
- Dense layer: Binary classification output (high/low emotional state).

---

## Results

| Metric | Value |
|-------|-------|
| Accuracy | ~98% |
| AUC | ~0.995 |

---

## Next Steps (Planned Enhancements)

- Replace binary classification with continuous regression.
- Multi-label outputs: Arousal, Valence, Dominance.
- EEG embeddings (Brain2Vec representation learning).
- Transformer encoder integration.
- Spectrogram-based CNN architectures.
- Contrastive learning (EEG-SimCLR).
- Cross-subject adaptation & generalization.
- Ensemble modeling.

---

## Git Ignore Justification

Large data files and checkpoints are excluded to keep the repo lightweight. Ignored items include:

data/
*.mat
*.npy
*.pt
*.pth

---

## Contributors

- **Vamsi Krishna Reddy** — Implementation, architecture recreation, training pipeline.

