import scipy.io as sio
import numpy as np

mat = sio.loadmat("data/deap/s02.mat", simplify_cells=True)

data = mat["data"]
print("data shape:", data.shape)

trial = data[0]
print("trial shape BEFORE slicing:", trial.shape)

trial32 = data[0][:32]
print("trial32 shape AFTER slicing:", trial32.shape)

print("total elements:", trial32.size)
