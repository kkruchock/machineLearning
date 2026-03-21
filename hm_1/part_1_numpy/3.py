import numpy as np

arr = np.random.randint(1, 101, (6, 6))
print(arr)

rows = np.arange(6).reshape(-1, 1)

result = np.where(
    (arr > 50) & (arr < 75) & ((arr % 5 == 0) | (rows % 2 == 0)), #считаем что первая строка - нулевая, то есть четная, как индексы
    0,
    arr
)

print(result)