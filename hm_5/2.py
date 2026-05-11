import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from skimage import data

# ============================================
# 1. ЗАГРУЗКА ИЗОБРАЖЕНИЯ
# ============================================
img = data.astronaut()  # 512x512, цветная
# img = data.chelsea()        # котик
# img = data.rocket()         # ракета

print(f"Размер изображения: {img.shape}")
print(f"Всего пикселей: {img.shape[0] * img.shape[1]}")

# ============================================
# 2. ПОДГОТОВКА ДАННЫХ (каждый пиксель → точка)
# ============================================
height, width, channels = img.shape

# Создаём координаты X, Y для каждого пикселя
X_coords, Y_coords = np.meshgrid(np.arange(width), np.arange(height))
X_coords = X_coords.flatten()
Y_coords = Y_coords.flatten()

# Превращаем изображение в массив пикселей (N, 3)
pixels = img.reshape(-1, 3)  # (262144, 3) для 512×512

# ============================================
# 3. ЭКСПЕРИМЕНТ С РАЗНЫМИ k (вес координат)
# ============================================
N_CLUSTERS = 16  # количество цветов на выходе (можно менять)
k_values = [0, 0.1, 0.5, 1.0, 2.0]  # вес координат

fig, axes = plt.subplots(1, len(k_values) + 1, figsize=(20, 4))

# Оригинальное изображение
axes[0].imshow(img)
axes[0].set_title('Оригинал')
axes[0].axis('off')

for idx, k in enumerate(k_values[::-1]):
    print(f"Обработка k = {k}...")

    # Формируем признаки: [R, G, B, k*X, k*Y]
    features = np.column_stack([
        pixels[:, 0],  # R
        pixels[:, 1],  # G
        pixels[:, 2],  # B
        k * X_coords,  # k * X
        k * Y_coords  # k * Y
    ])

    # K-Means кластеризация
    kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init=10)
    labels = kmeans.fit_predict(features)

    # Заменяем цвет каждого пикселя на цвет его кластера
    new_pixels = kmeans.cluster_centers_[labels][:, :3].astype(np.uint8)
    new_img = new_pixels.reshape(height, width, 3)

    # Визуализация
    axes[idx + 1].imshow(new_img)
    axes[idx + 1].set_title(f'k = {k}')
    axes[idx + 1].axis('off')

plt.tight_layout()
plt.show()