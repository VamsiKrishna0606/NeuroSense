import os
import numpy as np
import scipy.io as sio
from scipy.signal import butter, filtfilt

# ========================================
# CONSTANTS
# ========================================
FS = 128
CUTOFF = (4, 45)
WINDOW = 128
SHIFT = 128
REMOVE_SEC = 3
REMOVE_SAMPLES = FS * REMOVE_SEC

# ========================================
# BANDPASS FILTER
# ========================================
def butter_bandpass():
    nyq = 0.5 * FS
    low = CUTOFF[0] / nyq
    high = CUTOFF[1] / nyq
    return butter(4, [low, high], btype="band")

b, a = butter_bandpass()

def bandpass_filter(signals):
    """ signals: (32, N) """
    return filtfilt(b, a, signals, axis=1)

# ========================================
# WINDOWING
# ========================================
def create_windows(trial):
    """
    trial: (32, N)
    return: (32, W, 128)
    """
    windows = []
    for ch in range(trial.shape[0]):
        ch_data = trial[ch]
        ch_windows = []

        for start in range(0, len(ch_data) - WINDOW, SHIFT):
            seg = ch_data[start:start + WINDOW]
            seg = (seg - np.mean(seg)) / (np.std(seg) + 1e-6)
            ch_windows.append(seg)

        windows.append(np.array(ch_windows))

    return np.array(windows)   # (32, W, 128)

# ========================================
# PROCESS A SINGLE SUBJECT
# ========================================
def load_deap_subject(mat_data):
    """
    mat_data["data"]: (40, 40, 8064)
    mat_data["labels"]: (40, 4)
    returns: list-of-trials, list-of-labels
    """
    eeg = mat_data["data"][:, :32, :]    # (40, 32, 8064)
    labels = mat_data["labels"][:, 1]    # arousal (0–10)

    trials = []
    for trial in eeg:
        trial = trial[:, REMOVE_SAMPLES:]      # remove 3 sec
        trial = bandpass_filter(trial)         # filter
        windows = create_windows(trial)        # windowing
        trials.append(windows)

    # convert to binary labels
    bin_labels = (labels >= 5).astype(int)

    return trials, bin_labels.tolist()

# ========================================
# LOAD ALL SUBJECTS — FINAL PUBLIC API
# ========================================
def load_all_subjects(data_folder):
    """
    RETURNS:
      data["s01"] = list of trials (each: 32×W×128)
      labels["s01"] = [0/1, 0/1, ...] (40 values)
    """
    print(f"📥 Loading DEAP v2 from: {data_folder}")

    subjects_data = {}
    subjects_labels = {}

    files = sorted(os.listdir(data_folder))

    for file in files:
        if not file.endswith(".mat"):
            continue

        subject_id = file.replace(".mat", "")  # e.g., "s01"
        path = os.path.join(data_folder, file)

        mat = sio.loadmat(path, simplify_cells=True)

        trials, labels = load_deap_subject(mat)
        subjects_data[subject_id] = trials
        subjects_labels[subject_id] = labels

        print(f"  Loaded {subject_id}: {len(trials)} trials")

    print("✅ Finished preprocessing all subjects.")
    return subjects_data, subjects_labels
