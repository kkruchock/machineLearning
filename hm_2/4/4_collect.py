import requests
import time
import csv
from datetime import datetime
# п1 - ключ
API_KEY = ""
CITY = "Kemerovo"

url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
data = requests.get(url).json()

# п2 - анализ json
print(data)
print("\n" + "="*50)
print(f"Температура: {data['main']['temp']}")
print(f"Влажность: {data['main']['humidity']}")
print(f"Давление: {data['main']['pressure']}")

# имя файла для сохранения
FILENAME = "weather_data.csv"

# открываем файл для записи (добавляем заголовки один раз)
with open(FILENAME, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['datetime', 'temperature', 'humidity', 'pressure'])

# собираем 72 часа (3 дня) раз в час = 72 запроса
for i in range(72):
    # запрашиваем данные
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()

    # Берем нужные поля
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temp = data['main']['temp']
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']

    # Сохраняем в файл
    with open(FILENAME, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([now, temp, humidity, pressure])

    print(f"{i + 1}/72: {now} | {temp}°C | {humidity}% | {pressure} hPa")

    # Ждем 1 час до следующего запроса (кроме последнего)
    if i < 71:
        time.sleep(60)

print(f"\nГотово! Данные сохранены в {FILENAME}")