import scipy.io as sio

mat = sio.loadmat("data/deap/s02.mat", simplify_cells=True)

data = mat["data"]  # (40,40,8064)

trial = data[0]     # (40,8064)
trial32 = trial[:32]

print("trial32 shape:", trial32.shape)
print("length per channel:", trial32.shape[1])
print("is divisible by 252:", trial32.shape[1] % 252 == 0)
print("is divisible by 256:", trial32.shape[1] % 256 == 0)
print("is divisible by 128:", trial32.shape[1] % 128 == 0)
