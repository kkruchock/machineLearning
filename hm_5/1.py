import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans, DBSCAN
from sklearn.datasets import load_digits
from sklearn.manifold import TSNE
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import dendrogram, linkage

# ============================================
# готовим данные как в прошлой домашке
# ============================================

digits = load_digits()
X = digits.data
y = digits.target

# стандартизация
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCA для ускорения t-SNE
pca_for_tsne = PCA(n_components=30, random_state=42)
X_pca_30 = pca_for_tsne.fit_transform(X_scaled)

# t-SNE для разных perplexity (количесвто ближайших соседей, учитывающих)
perplexity_list = [10, 70, 150]  # для задания нужны 10, 70, 150
tsne_results = []  # сюда сохраним результаты

for perp in perplexity_list:
    print(f"t-SNE с perplexity = {perp}...")
    tsne = TSNE(n_components=2, perplexity=perp, random_state=42)
    X_tsne = tsne.fit_transform(X_pca_30)
    tsne_results.append(X_tsne)

# ============================================
# K-MEANS для данных после t-SNE И ГРАФИК ЛОКТЯ
# ============================================
'''
# список perplexity для подписей
perp_list = [10, 70, 150]
# цвета чтобы разделить
colors = ['blue', 'green', 'red']

plt.figure(figsize=(10, 6))

for idx, perp in enumerate(perp_list):
    # берем данные
    X_tsne = tsne_results[idx]

    # ДЛЯ ИНЕРЦИИ
    inertia = []
    K_range = range(2, 11)

    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_tsne) # для каждой точке записан номер кластера
        inertia.append(kmeans.inertia_)

    # Рисуем график
    plt.plot(K_range, inertia, 'o-', color=colors[idx], label=f'perplexity = {perp}')

# График локтя (инерция) по оси x K по y инерция (чем меньше инерация (сумма квадратов расстояний до центров ) тем лучше точки расположены)
# ищем резкий перепад после него невыгодно добавлять кластера
plt.xlabel('K (количество кластеров)')
plt.ylabel('Инерция (сумма квадратов расстояний)')
plt.title('Метод локтя для выбора оптимального K')
plt.legend()
plt.grid(True)
plt.show()

# оптимальные k по графикам локтя
# per   k
# 10	5
# 70	4
# 150	3-4

# ============================================
# ВИЗУАЛИЗАЦИЯ K-MEANS с оптимальным K (не понял надо или нет)
# ============================================

# Оптимальные K, которые мы определили по локтю
optimal_k = {
    10: 5,
    70: 4,
    150: 4 # для 150 можно взять 3 или 4, возьмём 4 для сравнения
}

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
perp_list = [10, 70, 150]

for i, perp in enumerate(perp_list):
    # Берём точки для этого perplexity
    X_tsne = tsne_results[i]
    k = optimal_k[perp]

    # Обучаем K-Means
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_tsne)

    # Рисуем
    scatter = axes[i].scatter(X_tsne[:, 0], X_tsne[:, 1], c=labels, cmap='tab10', s=10)
    axes[i].set_title(f'K-Means, perplexity = {perp}, K = {k}')
    axes[i].set_xlabel('t-SNE 1')
    axes[i].set_ylabel('t-SNE 2')
    axes[i].set_xticks([])
    axes[i].set_yticks([])

    # Добавляем цветовую шкалу
    plt.colorbar(scatter, ax=axes[i], label='Кластер')

plt.tight_layout()
plt.show()'''
'''
# ============================================
# DBSCAN: подбор eps с помощью k-distance plot
# ============================================

# параметры для подбора
min_samples = 4  # классическое значение, позже можно поменять (при 5 особо не меняетс)

perp_list = [10, 70, 150]
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for i, perp in enumerate(perp_list):
    X_tsne = tsne_results[i]

    # ищем расстояния до min_samples-го соседа для каждой точки
    neigh = NearestNeighbors(n_neighbors=min_samples)
    neigh.fit(X_tsne)
    distances, _ = neigh.kneighbors(X_tsne)

    # Сортируем расстояния по возрастанию
    k_dist = np.sort(distances[:, -1])

    # Рисуем график
    axes[i].plot(k_dist)
    axes[i].set_title(f'k-distance plot, perplexity = {perp}')
    axes[i].set_xlabel('Точки, отсортированные по расстоянию')
    axes[i].set_ylabel(f'Расстояние до {min_samples}-го соседа')
    axes[i].grid(True)

plt.tight_layout()
plt.show()

# ============================================
# DBSCAN кластеризация 
# ============================================

params = {
    10: {'eps': 2.5, 'min_samples': 4},
    70: {'eps': 1.3, 'min_samples': 4},
    150: {'eps': 0.75, 'min_samples': 4}
}

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
perp_list = [10, 70, 150]

for i, perp in enumerate(perp_list):
    X_tsne = tsne_results[i]
    eps = params[perp]['eps']
    min_samples = params[perp]['min_samples']

    # Обучаем DBSCAN
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(X_tsne)

    # Подсчитываем кластеры и шум
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)

    # Рисуем: шум — чёрным, кластеры — цветными
    unique_labels = set(labels)
    colors = plt.cm.tab10(np.linspace(0, 1, len(unique_labels)))

    for idx, label in enumerate(unique_labels):
        if label == -1:
            axes[i].scatter(X_tsne[labels == label, 0],
                            X_tsne[labels == label, 1],
                            c='black', s=10, label='шум')
        else:
            axes[i].scatter(X_tsne[labels == label, 0],
                            X_tsne[labels == label, 1],
                            c=[colors[idx]], s=10)

    axes[i].set_title(f'DBSCAN, perplexity = {perp}\neps={eps}, min_samples={min_samples}\n'
                      f'Кластеров: {n_clusters}, Шум: {n_noise} точек')
    axes[i].set_xlabel('t-SNE 1')
    axes[i].set_ylabel('t-SNE 2')
    axes[i].set_xticks([])
    axes[i].set_yticks([])

plt.tight_layout()
plt.show()'''

# ============================================
# ИЕРАРХИЧЕСКАЯ КЛАСТЕРИЗАЦИЯ (дендрограммы)
# ============================================

# Методы linkage для сравнения
methods = ['ward', 'complete', 'average', 'single']
perp_list = [10, 70, 150]

# Для каждого perplexity строим набор дендрограмм
for perp in perp_list:
    idx = perp_list.index(perp)
    X_tsne = tsne_results[idx]

    # потыкать разное кол-во точек
    X_sample = X_tsne[:1797]

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    axes = axes.ravel()

    for i, method in enumerate(methods):
        # Строим матрицу связей (linkage matrix)
        Z = linkage(X_sample, method=method)

        # Рисуем дендрограмму
        dendrogram(Z, ax=axes[i], truncate_mode='lastp', p=15, leaf_rotation=90)
        axes[i].set_title(f'perplexity = {perp}, method = {method}')
        axes[i].set_xlabel('Индекс точки (или кластер)')
        axes[i].set_ylabel('Расстояние объединения')

    plt.suptitle(f'Дендрограммы для perplexity = {perp}', fontsize=14)
    plt.tight_layout()
    plt.show()
