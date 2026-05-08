import matplotlib.pyplot as plt
import librosa.display

# ===== ЗАГРУЖАЕМ ФАЙЛ =====
audio_path = r"C:\Users\Дмитрий\Downloads\1-110389-A-0.wav"
data, sr = librosa.load(audio_path, sr=None)

print(f"Частота дискретизации: {sr} Гц")
print(f"Длительность файла: {len(data)/sr:.2f} секунд")

# ===== ПУНКТ 2: ГРАФИК АМПЛИТУДЫ =====
plt.figure(figsize=(14, 4))
librosa.display.waveshow(data, sr=sr)
plt.title("График амплитуды звуковой волны")
plt.xlabel("Время (секунды)")
plt.ylabel("Амплитуда")
plt.tight_layout()
plt.show()

# ===== ВВОДИМ УЧАСТОК С ЛАЕМ (глядя на график) =====
start = float(input("Введите время НАЧАЛА лая (в секундах): "))
end = float(input("Введите время КОНЦА лая (в секундах): "))

# Вырезаем участок
start_idx = int(start * sr)
end_idx = int(end * sr)
bark = data[start_idx:end_idx]

print(f"\nВырезан участок: {start:.2f} - {end:.2f} с")
print(f"Длительность участка: {len(bark)/sr:.2f} с")

# ===== ПУНКТ 3: СПЕКТРОГРАММА НАЙДЕННОГО УЧАСТКА =====
plt.figure(figsize=(14, 6))

X = librosa.stft(bark)
Xdb = librosa.amplitude_to_db(abs(X))

librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')
plt.colorbar(label='Интенсивность (dB)')
plt.title(f"Спектрограмма лая ({start:.2f} - {end:.2f} с)")
plt.tight_layout()
plt.show()