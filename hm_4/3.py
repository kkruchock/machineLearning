import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

digits = load_digits()
X = digits.data
y = digits.target

print(f"Размер данных: {X.shape} (1797 фото × 64 пикселя)")
print(f"Классов: {len(set(y))} (цифры 0-9)")

# ============================================
# ПУНКТ 1: PCA + исключение малозначимых признаков
# ============================================
print("\n" + "=" * 60)
print("ПУНКТ 1: PCA анализ и исключение малозначимых признаков")
print("=" * 60)

# Стандартизируем
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 1.1 PCA со ВСЕМИ компонентами
pca_full = PCA()
X_pca_full = pca_full.fit_transform(X_scaled)

# Смотрим, сколько дисперсии объясняет каждая компонента
print("\n--- Объяснённая дисперсия по компонентам ---")
for i in range(64):
    print(f"  PC{i + 1}: {pca_full.explained_variance_ratio_[i] * 100:.2f}%")

# Малозначимые, которые объясняют меньше 1% дисперсии
important_mask = pca_full.explained_variance_ratio_ > 0.01
n_important = sum(important_mask)

print(f"\n--- Исключение малозначимых признаков ---")
print(f"Всего компонент: {len(pca_full.explained_variance_ratio_)}")
print(f"Важных компонент (>1% дисперсии): {n_important}")
print(f"Исключено малозначимых: {len(pca_full.explained_variance_ratio_) - n_important}")

# Создаём PCA только с важными компонентами
pca_important = PCA(n_components=n_important)
X_pca_important = pca_important.fit_transform(X_scaled)

print(f"\nРазмер ДО: {X_scaled.shape}")
print(f"Размер ПОСЛЕ исключения малозначимых: {X_pca_important.shape}")

# Визуализация ДО и ПОСЛЕ (первые 2 компоненты для наглядности)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# ДО исключения (первые 2 компоненты всех)
axes[0].scatter(X_pca_full[:, 0], X_pca_full[:, 1], c=y, cmap='tab10', s=10)
axes[0].set_title(f'ДО: все {X_pca_full.shape[1]} компонент\n(показаны PC1 и PC2)')
axes[0].set_xlabel('PC1')
axes[0].set_ylabel('PC2')

# ПОСЛЕ исключения (первые 2 компоненты важных)
axes[1].scatter(X_pca_important[:, 0], X_pca_important[:, 1], c=y, cmap='tab10', s=10)
axes[1].set_title(f'ПОСЛЕ: только {n_important} важных компонент\n(показаны PC1 и PC2)')
axes[1].set_xlabel('PC1')
axes[1].set_ylabel('PC2')

plt.tight_layout()
plt.show()

# ============================================
# ПУНКТ 2: t-SNE с разными perplexity
# ============================================
print("\n" + "=" * 60)
print("ПУНКТ 2: t-SNE с разными perplexity")
print("=" * 60)

# Уменьшаем размерность через PCA до 30 компонент (для ускорения t-SNE)
pca_for_tsne = PCA(n_components=30, random_state=42)
X_pca_30 = pca_for_tsne.fit_transform(X_scaled)

# Пробуем разные perplexity
perplexity_list = [10, 30, 50, 70, 90]

fig, axes = plt.subplots(1, 5, figsize=(15, 4))

for i, perp in enumerate(perplexity_list):
    print(f"t-SNE с perplexity = {perp}...")
    # Убрали n_iter — теперь используется max_iter по умолчанию (1000)
    tsne = TSNE(n_components=2, perplexity=perp, random_state=42)
    X_tsne = tsne.fit_transform(X_pca_30)

    axes[i].scatter(X_tsne[:, 0], X_tsne[:, 1], c=y, cmap='tab10', s=5)
    axes[i].set_title(f'perplexity = {perp}')
    axes[i].set_xticks([])
    axes[i].set_yticks([])

plt.suptitle('t-SNE визуализация цифр с разными perplexity', fontsize=14)
plt.tight_layout()
plt.show()