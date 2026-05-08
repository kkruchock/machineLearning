from skimage.io import imread
import matplotlib.pyplot as plt
import numpy as np

# загружаем изображение
url = 'https://www.osp.ru/FileStorage/DOCUMENTS_ILLUSTRATIONS/13234504/original.jpg'
img = imread(url)

# получаем размеры изображения
height, width, channels = img.shape
print(f"Размер изображения: {width} x {height} пикселей")
print(f"Общая площадь изображения: {width * height} пикселей")

# вычисляем сторону квадрата, занимающего 10% площади
area = width * height
square_area = 0.1 * area
square_side = int(np.sqrt(square_area))  # округляем до целых пикселей
print(f"Площадь квадрата (10% от площади изображения): {square_area:.0f} пикселей²")
print(f"Сторона квадрата: {square_side} пикселей")

# определяем координаты для размещения квадрата в центре
center_x = width // 2
center_y = height // 2

# координаты левого верхнего угла квадрата
left = center_x - square_side // 2
top = center_y - square_side // 2
right = left + square_side
bottom = top + square_side

print(f"Квадрат будет расположен в области:")
print(f"  По горизонтали: пиксели {left} до {right}")
print(f"  По вертикали: пиксели {top} до {bottom}")

# рисуем белый квадрат
img[top:bottom, left:right, :] = [255, 255, 255]

# отображаем результат
plt.figure(figsize=(10, 8))
plt.imshow(img)
plt.title(f"Изображение с белым квадратом в центре (сторона = {square_side} пикселей, 10% площади)")
plt.show()