import scipy.io as sio
import numpy as np

print("\n========================================")
print("     PHASE-4 MULTIBAND SHAPE CHECK")
print("========================================")

path = "data/deap/s01.mat"

mat = sio.loadmat(path)

data = mat["data"]
labels = mat["labels"]

print("RAW data shape:", data.shape)      # Expect (40, 40, 8064)
print("RAW labels shape:", labels.shape)

# Take only 32 channels
eeg = data[:, :32, :]
print("AFTER channel trim:", eeg.shape)  # (40, 32, 8064)

# Check one trial
trial0 = eeg[0]
print("One trial shape:", trial0.shape)  # (32, 8064)
