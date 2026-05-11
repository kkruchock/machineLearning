import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data"

# из документации
columns = [
    'symboling', 'normalized-losses', 'make', 'fuel-type', 'aspiration',
    'num-of-doors', 'body-style', 'drive-wheels', 'engine-location',
    'wheel-base', 'length', 'width', 'height', 'curb-weight', 'engine-type',
    'num-of-cylinders', 'engine-size', 'fuel-system', 'bore', 'stroke',
    'compression-ratio', 'horsepower', 'peak-rpm', 'city-mpg', 'highway-mpg',
    'price'
]

df = pd.read_csv(url, header=None, names=columns, na_values='?')

print(f"Размер: {df.shape[0]} строк, {df.shape[1]} столбцов")
print(f"Столбцы: {df.columns.tolist()}")
print("\nПервые 3 строки:")
print(df.head(3))

print("\n=== ОБРАБОТКА ПРОПУСКОВ ===")

print("Пропуски до обработки:")
print(df.isnull().sum())


# для числовых столбцов заполняем пропуски медианой (устойчива к выбросам)
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
for col in numeric_cols:
    median_val = df[col].median()
    df[col] = df[col].fillna(median_val)

# для категориальных столбцов заполняем модой
categorical_cols = df.select_dtypes(include=['object', 'string']).columns
for col in categorical_cols:
    mode_val = df[col].mode()[0]
    df[col] = df[col].fillna(mode_val)

print("\nПропуски после обработки:")
print(df.isnull().sum())

print("\n=== МАСШТАБИРОВАНИЕ ===")

# Выбираем только числовые столбцы для масштабирования
# (категориальные пока не трогаем)
numeric_df = df[numeric_cols].copy()

# MinMaxScaler (нормализация к [0, 1])
scaler_mm = MinMaxScaler()
numeric_mm = scaler_mm.fit_transform(numeric_df)
df_mm = pd.DataFrame(numeric_mm, columns=numeric_cols)

# StandardScaler (стандартизация: среднее=0, std=1)
scaler_std = StandardScaler()
numeric_std = scaler_std.fit_transform(numeric_df)
df_std = pd.DataFrame(numeric_std, columns=numeric_cols)

print("Исходные данные (первые 3 строки, числовые столбцы):")
print(numeric_df.head(3))
print("\nПосле MinMaxScaler (диапазон 0-1):")
print(df_mm.head(3))
print("\nПосле StandardScaler (среднее=0, отклонение=1):")
print(df_std.head(3))

print("\n=== КОРРЕЛЯЦИОННЫЙ АНАЛИЗ ===")

# Матрица корреляций ДО
corr_before = numeric_df.corr()

# Визуализация
plt.figure(figsize=(14, 12))
sns.heatmap(corr_before, annot=False, cmap='coolwarm', center=0)
plt.title('Матрица корреляций ДО создания нового признака')
plt.tight_layout()
plt.show()

# Находим сильно коррелирующие пары
print("Сильно коррелирующие пары (|r| > 0.7):")
for i in range(len(corr_before.columns)):
    for j in range(i+1, len(corr_before.columns)):
        if abs(corr_before.iloc[i, j]) > 0.7:
            print(f"  {corr_before.columns[i]} — {corr_before.columns[j]}: {corr_before.iloc[i, j]:.3f}")

print("\n=== СОЗДАНИЕ НОВЫХ ПРИЗНАКОВ ===")

# Копируем исходные числовые данные
df_with_new = numeric_df.copy()

# Объединяем: wheel-base, length, width, curb-weight
df_with_new['size_index'] = (
    df_with_new['wheel-base'] * 0.25 +
    df_with_new['length'] * 0.25 +
    df_with_new['width'] * 0.25 +
    df_with_new['curb-weight'] * 0.25
)

print("\n=== КОРРЕЛЯЦИИ ПОСЛЕ СОЗДАНИЯ ПРИЗНАКОВ ===")

# Добавляем новые признаки в DataFrame для корреляции
numeric_with_new = df_with_new.copy()

numeric_with_new = numeric_with_new.drop(columns=['city-mpg', 'highway-mpg'], errors='ignore')

# Матрица корреляций
corr_after = numeric_with_new.corr()

# Визуализация
plt.figure(figsize=(16, 14))
sns.heatmap(corr_after, annot=False, cmap='coolwarm', center=0)
plt.title('Матрица корреляций ПОСЛЕ создания новых признаков', fontsize=14)
plt.tight_layout()
plt.show()

print("\n=== PCA АНАЛИЗ ===")

# Удаляем старые признаки (которые объединили)
features_to_drop = ['wheel-base', 'length', 'width', 'curb-weight',
                    'city-mpg', 'highway-mpg']

df_final = df_with_new.drop(columns=features_to_drop, errors='ignore')


X = StandardScaler().fit_transform(df_final)

pca = PCA()
X_pca = pca.fit_transform(X)

# дисперсия
explained_variance = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(explained_variance)

print("\nТОП-5 главных компонент и их вклад в дисперсию:")
for i in range(min(5, len(explained_variance))):
    print(f"  PC{i+1}: {explained_variance[i]:.4f} ({explained_variance[i]*100:.2f}%)")

# кумулятивная кривая
plt.figure(figsize=(10, 6))
plt.bar(range(1, len(explained_variance)+1), explained_variance,
        alpha=0.6, color='steelblue', label='Доля дисперсии')
plt.plot(range(1, len(cumulative_variance)+1), cumulative_variance,
         'ro-', linewidth=2, label='Кумулятивная дисперсия')
plt.axhline(y=0.95, color='red', linestyle='--', alpha=0.7, label='95% дисперсии')

n_components_95 = np.argmax(cumulative_variance >= 0.95) + 1
plt.axvline(x=n_components_95, color='green', linestyle='--', alpha=0.7,
            label=f'95% дисперсии: {n_components_95} компонент')

plt.xlabel('Номер главной компоненты', fontsize=12)
plt.ylabel('Доля объяснённой дисперсии', fontsize=12)
plt.title('Кумулятивная кривая дисперсии (PCA)', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print(f"\nДля сохранения 95% дисперсии достаточно {n_components_95} главных компонент.")