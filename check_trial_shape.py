import scipy.io as sio
import numpy as np

from preprocessing.deap_multiband import process_one_trial

print("\n========================================")
print("     PHASE-4 WINDOWING CHECK")
print("========================================")

mat = sio.loadmat("data/deap/s01.mat")

raw = mat["data"][:, :32, :]   # (40, 32, 8064)
trial0 = raw[0]                # (32, 8064)

print("Input trial shape:", trial0.shape)

processed = process_one_trial(trial0)

print("\nProcessed shape:", processed.shape)
print("(32 channels, W windows, 4 bands, 128 samples)")
