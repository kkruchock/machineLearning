from datetime import datetime, timedelta

import numpy as np
import matplotlib.pyplot as plt

# 1
days = 365
stations = 100
parameters = 3

weather_data = np.zeros((days, stations, parameters))

weather_data[:, :, 0] = np.random.uniform(-20, 40, (days, stations))
weather_data[:, :, 1] = np.random.uniform(20, 90, (days, stations))
weather_data[:, :, 2] = np.random.uniform(950, 1050, (days, stations))

# 2
print("\n---2---")

mean_temperature = np.mean(weather_data[:, :, 0])
mean_humidity = np.mean(weather_data[:, :, 1])
mean_pressure = np.mean(weather_data[:, :, 2])

print(f"Средняя температура: {mean_temperature:.2f}°C")
print(f"Средняя влажность: {mean_humidity:.2f}%")
print(f"Среднее давление: {mean_pressure:.2f} hPa")

# 3
print("\n---3---")
max_temperature = np.max(weather_data[:, :, 0])
min_temperature = np.min(weather_data[:, :, 0])

temperature_extremes = (max_temperature, min_temperature)

print(f"максимальная температура: {max_temperature:.2f}°C")
print(f"минимальная температура: {min_temperature:.2f}°C")
print(f"кортеж: {temperature_extremes}")

# 4
print("\n---4---")

station_avg_pressure = np.mean(weather_data[:, :, 2], axis=0)

station_index = np.argmax(station_avg_pressure)

print(f"станция с наибольшим средним давлением: {station_index}")
print(f"среднее давление на этой станции: {station_avg_pressure[station_index]:.2f} hPa")

# 5
print("\n---5---")
threshold = 40
daily_avg_humidity = weather_data[:, :, 1].mean(axis=1)
low_humidity_days = np.where(daily_avg_humidity < threshold)[0]
print(f"дни с влажностью ниже {threshold}%: {low_humidity_days}")

# 6
print("\n---6---")

param_min = weather_data.min(axis=(0, 1))
param_max = weather_data.max(axis=(0, 1))

weather_norm = (weather_data - param_min) / (param_max - param_min)

# 7
print("\n---7---")

weather_flat = weather_data.reshape(-1, parameters)

correlation_matrix = np.corrcoef(weather_flat.T)

print(correlation_matrix)
print(f"  [0,1] = {correlation_matrix[0,1]:.3f}  -> температура vs влажность")
print(f"  [0,2] = {correlation_matrix[0,2]:.3f}  -> температура vs давление")
print(f"  [1,2] = {correlation_matrix[1,2]:.3f}  -> влажность vs давление")

# 8
print("\n---8---")

avg_hum = weather_data[:, :, 1].mean(axis=1)
avg_pres = weather_data[:, :, 2].mean(axis=1)
max_temp = weather_data[:, :, 0].max(axis=1)

special_days = np.where((avg_hum < 40) & (avg_pres > 1020) & (max_temp > 35))[0]

print(f"Дни со всеми условиями: {special_days}")
print(f"Количество: {len(special_days)}")

# 9
print("\n---9--- ВИЗУАЛИЗАЦИЯ")

# График 1: Тепловая карта среднего давления по станциям
plt.figure(1, figsize=(8, 6))
pressure_map = station_avg_pressure.reshape(10, 10)
plt.imshow(pressure_map, cmap='RdYlBu_r', aspect='equal')
plt.colorbar(label='Давление (hPa)')
plt.title('Среднее атмосферное давление по станциям')
plt.xlabel('Станции (10x10 сетка)')
plt.ylabel('Станции (10x10 сетка)')
plt.show()

fig = plt.figure(2, figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Берем каждый 10-й день и каждую 10-ю станцию
day_indices = np.arange(0, days, 10)
station_indices = np.arange(0, stations, 10)

X, Y = np.meshgrid(station_indices, day_indices)
Z = weather_data[day_indices[:, np.newaxis], station_indices, 0]

surf = ax.plot_surface(X, Y, Z, cmap='coolwarm', edgecolor='none')
ax.set_xlabel('Номер станции')
ax.set_ylabel('День года')
ax.set_zlabel('Температура (°C)')
ax.set_title('Сезонные изменения температуры\n(по дням и станциям)')
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='Температура (°C)')
plt.show()

# 10 - ПРЕОБРАЗОВАНИЕ В DATETIME И АНОМАЛИИ
print("\n---10--- ДАТЫ И АНОМАЛИИ")

# Создаем массив дат
start_date = datetime(2024, 1, 1)
dates = np.array([start_date + timedelta(days=i) for i in range(days)])

# Среднесуточная температура
daily_temp = weather_data[:, :, 0].mean(axis=1)

# Группируем по месяцам (1-12)
monthly_anomalies = []
for month in range(1, 13):
    month_mask = np.array([d.month == month for d in dates])
    month_temps = daily_temp[month_mask]

    if len(month_temps) > 0:
        month_mean = np.mean(month_temps)
        month_std = np.std(month_temps)

        # Аномалии: отклонение > 2 стандартных отклонений
        anomalies = month_temps[(month_temps > month_mean + 2 * month_std) |
                                (month_temps < month_mean - 2 * month_std)]

        print(f"Месяц {month}: среднее={month_mean:.1f}°C, стд={month_std:.1f}, аномалий={len(anomalies)}")
        monthly_anomalies.append(len(anomalies))

print(f"\nВсего аномальных дней: {sum(monthly_anomalies)}")