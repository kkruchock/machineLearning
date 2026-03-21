import numpy as np

arr = np.random.randint(1, 101, (10, 10))
arr_norm = 2 * (arr - arr.min()) / (arr.max() - arr.min()) - 1

np.savetxt('result.txt', arr_norm, fmt='%.6f')