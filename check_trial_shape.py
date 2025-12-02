from preprocessing.deap_subject_loader import load_all_subjects
import torch

data, labels = load_all_subjects("data/deap")
x = data["s01"][0]   # first sample from subject 1
print(x.shape)
