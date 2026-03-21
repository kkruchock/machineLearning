import numpy as np

arr_2 = np.random.randint(1, 101, size=(5, 5))
print(arr_2)

arr_1 = arr_2.reshape(-1)
print(arr_1)

arr_sorted_asc = np.sort(arr_1)
print(arr_sorted_asc)

indices_desc = np.argsort(arr_1)[::-1]
arr_sorted_desc = arr_1[indices_desc]
print(arr_sorted_desc)

unique_values, counts = np.unique(arr_1, return_counts=True)
print("уникальные элементы:", unique_values)
print("частота:", counts)