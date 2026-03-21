import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Загрузка
img = Image.open('test.jpg')
arr = np.array(img)

# Ввод параметров
y_min, y_max = map(int, input("y_min y_max: ").split())
x_min, x_max = map(int, input("x_min x_max: ").split())
h = int(input("h: "))

# Вырезаем область
region = arr[y_min:y_max, x_min:x_max]

# Размеры блоков
h_block = region.shape[0] // h
w_block = region.shape[1] // h

# Обрезаем до кратного
region = region[:h*h_block, :h*w_block]

# Группируем и усредняем
reshaped = region.reshape(h, h_block, h, w_block, -1)
averaged = reshaped.mean(axis=(1, 3)).astype(np.uint8)

# Разворачиваем обратно
result = arr.copy()
for i in range(h):
    for j in range(h):
        result[y_min + i*h_block:y_min + (i+1)*h_block,
               x_min + j*w_block:x_min + (j+1)*w_block] = averaged[i, j]

# Показываем
plt.imshow(result)
plt.show()