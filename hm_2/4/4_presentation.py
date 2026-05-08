import pandas as pd
import matplotlib.pyplot as plt

CITY = "Kemerovo"

# Загружаем данные из файла
df = pd.read_csv("weather_data.csv")
df['datetime'] = pd.to_datetime(df['datetime'])

# Рисуем три графика на одной картинке
fig, ax1 = plt.subplots(figsize=(14, 6))

# График температуры (синий)
ax1.plot(df['datetime'], df['temperature'], 'b-o', linewidth=1, markersize=3)
ax1.set_xlabel('Дата и время')
ax1.set_ylabel('Температура (°C)', color='b')
ax1.tick_params(axis='y', labelcolor='b')

# График влажности (зеленый) - своя шкала справа
ax2 = ax1.twinx()
ax2.plot(df['datetime'], df['humidity'], 'g-s', linewidth=1, markersize=3)
ax2.set_ylabel('Влажность (%)', color='g')
ax2.tick_params(axis='y', labelcolor='g')

# График давления (красный) - своя шкала справа
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 70))
ax3.plot(df['datetime'], df['pressure'], 'r-^', linewidth=1, markersize=3)
ax3.set_ylabel('Давление (гПа)', color='r')
ax3.tick_params(axis='y', labelcolor='r')

# Оформление
plt.title(f'Погода в городе {CITY} за 3 дня')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()