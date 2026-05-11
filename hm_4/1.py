from sklearn.datasets import make_blobs, make_circles
import matplotlib.pyplot as plt

X_blobs, y_blobs = make_blobs(
    n_samples=500, # 500 точек
    n_features=2, # 2 координаты
    centers=3, # 3 кластера
    cluster_std=0.6, # разброс
    random_state=42
)

X_circles, y_circles = make_circles(
    n_samples=450, # 450 точек
    factor=0.5, # радиус внутренней окружности = 0.5 * внешнего радиуса
    noise=0.05, # добавляем немного шума (точки не идеально на окружности)
    random_state=42
)

X_circles = X_circles * 10 # умножаем корды на 10

# создаём фигуру и оси (один рисунок)
plt.figure(figsize=(10, 8))

# кластеры
# X_blobs[:, 0] — все строки, столбец 0 (координата x)
# X_blobs[:, 1] — все строки, столбец 1 (координата y)
# s=20 — размер точки
# alpha=0.7 — прозрачность 70% (немного видно сквозь точки)
# label='Blobs' — подпись для легенды
plt.scatter(X_blobs[:, 0], X_blobs[:, 1],
            c='red', s=20, alpha=0.7, label='Blobs (кластеры)')

# круги
plt.scatter(X_circles[:, 0], X_circles[:, 1],
            c='green', s=20, alpha=0.7, label='Circles (кольца)')

# подписи к осям
plt.xlabel('X координата', fontsize=12)
plt.ylabel('Y координата', fontsize=12)

# заголовок
plt.title('Сравнение данных: make_blobs (красный) vs make_circles×10 (зелёный)', fontsize=14)

# легенда
plt.legend()

# сетка для удобства
plt.grid(True, alpha=0.3)

# показать
plt.show()