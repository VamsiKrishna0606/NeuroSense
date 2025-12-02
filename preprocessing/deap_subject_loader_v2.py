import os
import numpy as np
from scipy.signal import butter, filtfilt

# -----------------------------
# CONSTANTS
# -----------------------------
FS = 128               # DEAP sampling rate
CUTOFF = (4, 45)       # bandpass
WINDOW = 128           # window size
SHIFT = 128            # non-overlapping
REMOVAL_SECONDS = 3    # remove first 3 sec
REMOVE_SAMPLES = FS * REMOVAL_SECONDS


# -----------------------------
# 1. Bandpass filter design
# -----------------------------
def butter_bandpass():
    nyquist = 0.5 * FS
    low = CUTOFF[0] / nyquist
    high = CUTOFF[1] / nyquist
    return butter(4, [low, high], btype="band")


b, a = butter_bandpass()


def bandpass_filter(signals):
    """Apply bandpass filter to all channels"""
    return filtfilt(b, a, signals, axis=1)


# -----------------------------
# 2. Windowing function
# -----------------------------
def create_windows(trial):
    """
    Input trial: shape (32, N)
    Return: (32, num_windows, 128)
    """
    windows = []
    for ch in range(trial.shape[0]):
        channel_data = trial[ch]

        ch_windows = []
        for start in range(0, len(channel_data) - WINDOW, SHIFT):
            segment = channel_data[start:start + WINDOW]

            # normalize each window
            segment = (segment - np.mean(segment)) / (np.std(segment) + 1e-6)

            ch_windows.append(segment)

        windows.append(np.array(ch_windows))

    return np.array(windows)  # (32, W, 128)


# -----------------------------
# 3. Main loader function
# -----------------------------
def load_deap_subject_v2(mat_data):
    """
    mat_data["data"] shape: (40 trials, 40 channels, 8064 samples)
    We keep ONLY the first 32 EEG channels.
    """

    eeg_data = mat_data["data"][:, :32, :]   # -> (40, 32, 8064)
    labels = mat_data["labels"][:, 0]        # valence labels

    processed_trials = []

    for trial in eeg_data:
        # Remove first 3 seconds
        trial = trial[:, REMOVE_SAMPLES:]

        # Apply bandpass
        trial = bandpass_filter(trial)

        # Window into 128 segments
        windows = create_windows(trial)

        processed_trials.append(windows)

    return processed_trials, labels.tolist()
