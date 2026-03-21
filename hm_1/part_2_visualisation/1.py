import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image

img = Image.open('test.jpg')
arr = np.array(img)


def compress(img_arr, k):
    h, w = img_arr.shape[0] // k * k, img_arr.shape[1] // k * k #чтобы сжималось без остатка
    img_arr = img_arr[:h, :w]

    # Группировка и усреднение
    h_new, w_new = h // k, w // k
    reshaped = img_arr.reshape(h_new, k, w_new, k, -1)
    return reshaped.mean(axis=(1, 3)).astype(np.uint8)


# Применяем
k = int(input("Введите коэффициент сжатия k: "))
compressed = compress(arr, k)

# Показываем
plt.imshow(compressed)
plt.show()
px.imshow(compressed).show()