import scipy.io as sio

mat = sio.loadmat("data/deap/s02.mat", simplify_cells=True)
print("data shape:", mat["data"].shape)
