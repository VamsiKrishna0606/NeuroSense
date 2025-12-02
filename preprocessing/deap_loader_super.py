import numpy as np
import os
import scipy.io as sio
from scipy.signal import butter, filtfilt

FS = 128

# Raw windowing (best: preprocess-v2)
RAW_WINDOW = 128
RAW_SHIFT = 128
REMOVE_SEC = 3
REMOVE_SAMPLES = FS * REMOVE_SEC

# Multiband filters
BANDS = {
    "theta": (4, 7),
    "alpha": (8, 13),
    "beta": (14, 30),
    "gamma": (31, 45)
}

MB_WINDOW = 128
MB_SHIFT = 128


# ---------------------------------------------------------
# Butterworth filter
# ---------------------------------------------------------
def butter_bandpass(low, high):
    nyq = 0.5 * FS
    low /= nyq
    high /= nyq
    b, a = butter(4, [low, high], btype='band')
    return b, a


def apply_band_filter(signal, low, high):
    b, a = butter_bandpass(low, high)
    return filtfilt(b, a, signal)


# ---------------------------------------------------------
# Windowing helper
# ---------------------------------------------------------
def create_windows(signal, win, shift):
    windows = []
    for start in range(0, len(signal) - win + 1, shift):
        seg = signal[start:start + win]
        seg = (seg - np.mean(seg)) / (np.std(seg) + 1e-6)
        windows.append(seg)
    return np.array(windows)  # (W, win)


# ---------------------------------------------------------
# Process raw EEG (temporal branch)
# ---------------------------------------------------------
def process_raw_trial(trial):
    """
    Input trial: (32, 8064)
    Output: RAW = (32, 59, 128)
    """
    trial = trial[:, REMOVE_SAMPLES:]  # remove first 3 seconds

    ch_raw = []
    for ch in range(32):
        sig = trial[ch]
        windows = create_windows(sig, RAW_WINDOW, RAW_SHIFT)  # (59,128)
        ch_raw.append(windows)

    return np.array(ch_raw)  # (32,59,128)


# ---------------------------------------------------------
# Multiband spectral branch
# ---------------------------------------------------------
def process_multiband_trial(trial):
    """
    Input trial: (32,8064)
    Output: MULTIBAND = (32, W, 4, 128)
    """
    trial = trial[:, REMOVE_SAMPLES:]

    ch_out = []
    for ch in range(32):
        sig = trial[ch]
        band_list = []

        for (low, high) in BANDS.values():
            filtered = apply_band_filter(sig, low, high)
            win = create_windows(filtered, MB_WINDOW, MB_SHIFT)  # (W,128)
            band_list.append(win)

        band_array = np.stack(band_list, axis=1)  # (W,4,128)
        ch_out.append(band_array)

    return np.array(ch_out)  # (32,W,4,128)


# ---------------------------------------------------------
# Load entire DEAP dataset
# ---------------------------------------------------------
def load_super_deap(data_path):
    """
    Returns:
        raw_data["s01"]        = list of raw trials   (32,59,128)
        mb_data["s01"]         = list of multiband    (32,W,4,128)
        labels["s01"]          = list of 0/1
    """
    raw_data = {}
    mb_data = {}
    labels = {}

    for i in range(1, 33):
        fname = f"s{i:02d}.mat"
        path = os.path.join(data_path, fname)

        print(f"[DEAP SUPER] Loading {fname} ...")

        mat = sio.loadmat(path)
        raw = mat["data"][:, :32, :]      # (40,32,8064)
        labs = mat["labels"][:, 0]        # (40,)

        raw_trials = []
        mb_trials = []
        bin_labels = []

        for t in range(40):
            trial = raw[t]

            rt = process_raw_trial(trial)          # (32,59,128)
            mb = process_multiband_trial(trial)    # (32,W,4,128)

            raw_trials.append(rt)
            mb_trials.append(mb)

            bin_labels.append(1 if labs[t] >= 5 else 0)

        sid = f"s{i:02d}"
        raw_data[sid] = raw_trials
        mb_data[sid] = mb_trials
        labels[sid] = bin_labels

    print("✔ DEAP SUPER loading completed.")
    return raw_data, mb_data, labels
