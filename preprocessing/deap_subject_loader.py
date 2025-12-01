import os
import scipy.io as sio
import numpy as np
import torch
from scipy.signal import butter, filtfilt
from functools import lru_cache

# -----------------------------------------------------------
# OPTIONAL BANDPASS FILTER (4–45 Hz)
# -----------------------------------------------------------
def butter_bandpass(lowcut=4, highcut=45, fs=128, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    return butter(order, [low, high], btype='band')

def apply_bandpass(signal, fs=128):
    b, a = butter_bandpass()
    return filtfilt(b, a, signal)


# -----------------------------------------------------------
# Convert raw 8064 samples → (63, 128)
# -----------------------------------------------------------
def reshape_eeg(channel_signal):
    """
    channel_signal: (8064,)
    output: (63, 128)
    """
    return channel_signal.reshape(63, 128)


# -----------------------------------------------------------
# MAIN LOADER
# -----------------------------------------------------------
def load_all_subjects(data_folder):
    """
    Returns:
    data["s01"]   -> list of tensors, shape (1, 32, 63, 128)
    labels["s01"] -> list of 0/1 labels
    """

    print(f"\n📥 Loading DEAP from: {data_folder}")

    subjects_data = {}
    subjects_labels = {}

    files = sorted([f for f in os.listdir(data_folder) if f.endswith(".mat")])

    for file in files:
        subject_id = file.replace(".mat", "")   # "s01"
        path = os.path.join(data_folder, file)

        mat = sio.loadmat(path, simplify_cells=True)

        eeg = mat["data"]      # (40 trials, 40 channels, 8064 samples)
        labels = mat["labels"] # (40 trials, 4 labels)

        subject_tensors = []
        subject_targets = []

        # Arousal label
        arousal = labels[:, 1]
        binary_labels = (arousal >= 5).astype(int)

        for trial_idx in range(40):

            # --- take first 32 channels only ---
            trial = eeg[trial_idx][:32]         # (32, 8064)

            processed_channels = []

            for c in range(32):
                signal = trial[c]

                # OPTIONAL – enable if needed
                # signal = apply_bandpass(signal)

                # normalize channel
                signal = (signal - signal.mean()) / (signal.std() + 1e-6)

                # reshape 8064 → (63, 128)
                signal_reshaped = reshape_eeg(signal)   # (63, 128)

                processed_channels.append(signal_reshaped)

            # stack channels → shape (32, 63, 128)
            arr = np.stack(processed_channels)

            # final tensor → (1, 32, 63, 128)
            tensor = torch.tensor(arr, dtype=torch.float32).unsqueeze(0)

            subject_tensors.append(tensor)
            subject_targets.append(int(binary_labels[trial_idx]))

        subjects_data[subject_id] = subject_tensors
        subjects_labels[subject_id] = subject_targets

        print(f"  Loaded {subject_id}: {len(subject_tensors)} samples")

    print("✅ Finished loading all subjects.\n")
    return subjects_data, subjects_labels
