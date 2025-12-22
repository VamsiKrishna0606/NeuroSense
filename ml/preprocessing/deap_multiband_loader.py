import scipy.io as sio

def load_deap_subject_multiband(file_path):
    """
    Expected real DEAP: data = (40 trials, 40 channels, 8064)
    We keep only first 32 EEG channels.
    """

    mat = sio.loadmat(file_path)
    raw_data = mat["data"]      # (40, 40, 8064)
    raw_labels = mat["labels"]  # (40, 4)

    # keep only EEG channels (first 32)
    eeg_data = raw_data[:, :32, :]   # (40, 32, 8064)
    
    # get valence labels
    labels = (raw_labels[:, 0] >= 5).astype(int).tolist()

    return eeg_data, labels
