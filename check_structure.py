import scipy.io as sio

m = sio.loadmat("data/deap/s01.mat")

print("\n==== MAT CONTENTS ====")
for k, v in m.items():
    if not k.startswith("__"):
        print(k, type(v), getattr(v, "shape", None))

print("\n==== INSIDE mat['data'] ====")
print("type:", type(m["data"]))
print("shape:", getattr(m["data"], "shape", None))

item = m["data"][0]
print("\nFirst element type:", type(item))
print("Shape:", getattr(item, "shape", None))

try:
    print("\nItem[0] type:", type(item[0]))
    print("Shape:", getattr(item[0], "shape", None))
except:
    print("\nItem[0] not indexable.")
