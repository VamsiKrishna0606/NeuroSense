import numpy as np
from scipy.signal import butter, filtfilt
import os
import scipy.io as sio

FS = 128

# Frequency bands
BANDS = {
    "theta": (4, 7),
    "alpha": (8, 13),
    "beta": (14, 30),
    "gamma": (31, 45)
}

WINDOW = 128   # 1 second window
SHIFT = 128    # no overlap
REMOVE_SEC = 3
REMOVE_SAMPLES = FS * REMOVE_SEC


def butter_bandpass(low, high):
    nyq = 0.5 * FS
    low /= nyq
    high /= nyq
    b, a = butter(4, [low, high], btype='band')
    return b, a


def apply_band_filter(signal, low, high):
    b, a = butter_bandpass(low, high)
    return filtfilt(b, a, signal)  # filter each channel 1D


def create_windows(signal):
    """
    Create windows of shape (num_windows, 128)
    """
    windows = []
    for start in range(0, len(signal) - WINDOW + 1, SHIFT):
        seg = signal[start:start + WINDOW]
        seg = (seg - np.mean(seg)) / (np.std(seg) + 1e-6)
        windows.append(seg)
    return np.array(windows)  # (W, 128)


def process_one_trial(trial):
    """
    Input trial: (32, 8064)
    Output: (32, W, 4, 128)
    """
    trial = trial[:, REMOVE_SAMPLES:]  # remove first 3 secs

    channel_outputs = []

    for ch in range(32):
        ch_data = trial[ch]

        band_list = []

        for (low, high) in BANDS.values():
            filtered = apply_band_filter(ch_data, low, high)
            win = create_windows(filtered)  # (W, 128)
            band_list.append(win)

        band_array = np.stack(band_list, axis=1)  # (W, 4, 128)
        channel_outputs.append(band_array)

    return np.array(channel_outputs)  # (32, W, 4, 128)

def load_multiband_dataset(data_path):
    """
    Loads all 32 DEAP subjects and returns:
        data   = { "s01": [ trials ], ... }
        labels = { "s01": [0/1 labels], ... }
    """

    subjects = {}
    subject_labels = {}

    for i in range(1, 33):
        fname = f"s{i:02d}.mat"
        fpath = os.path.join(data_path, fname)

        print(f"[Multiband] Loading {fname} ...")

        mat = sio.loadmat(fpath)
        raw_data = mat["data"][:, :32, :]   # (40, 32, 8064)
        raw_labels = mat["labels"][:, 0]    # (40,)

        processed_trials = []
        bin_labels = []

        for t in range(len(raw_data)):
            trial = raw_data[t]
            processed = process_one_trial(trial)  # (32, W, 4, 128)
            processed_trials.append(processed)

            # Binary label mapping (same as LOSO):
            label = 1 if raw_labels[t] >= 5 else 0
            bin_labels.append(label)

        subjects[f"s{i:02d}"] = processed_trials
        subject_labels[f"s{i:02d}"] = bin_labels

    print("✔ Finished loading all subjects for multiband.")
    return subjects, subject_labels
