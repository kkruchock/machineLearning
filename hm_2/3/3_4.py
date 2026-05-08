"""
ЗАДАНИЕ 3, ПУНКТ 4:
Автоматическое удаление тихих участков (тишины)
"""

import numpy as np
import matplotlib.pyplot as plt
import librosa.display
import soundfile as sf

audio_path = r"C:\Users\Дмитрий\Downloads\1-110389-A-0.wav"  # ← тот же путь
data, sr = librosa.load(audio_path, sr=None)

# вычисляем громкость в маленьких окнах
# если громкость ниже порога (% от max) — это тишина, удаляем

# размер окна для анализа (0.05 секунды)
window_size = int(sr * 0.05)

# вычисляем среднюю громкость в каждом окне
rms = []
for i in range(0, len(data) - window_size, window_size):
    window = data[i:i+window_size]
    rms_value = np.sqrt(np.mean(window**2))
    rms.append(rms_value)

rms = np.array(rms)

# считаем тишиной всё, что тише 3% от максимальной громкости
threshold = 0.03 * np.max(rms)

# Находим, какие окна НЕ являются тишиной (содержат звук)
sound_windows = rms > threshold

# Если окно со звуком — оставляем, если тишина — удаляем
audio_cleaned = []
for i, is_sound in enumerate(sound_windows):
    if is_sound:
        start = i * window_size
        end = start + window_size
        audio_cleaned.extend(data[start:end])

audio_cleaned = np.array(audio_cleaned)

# ===== ВИЗУАЛИЗАЦИЯ РЕЗУЛЬТАТА =====
fig, axes = plt.subplots(2, 1, figsize=(14, 6))

# Оригинал
axes[0].plot(np.arange(len(data)) / sr, data, 'b-', linewidth=0.5)
axes[0].set_title(f"Оригинал (длина: {len(data)/sr:.2f} с)")
axes[0].set_ylabel("Амплитуда")
axes[0].grid(True, alpha=0.3)

# Очищенный
axes[1].plot(np.arange(len(audio_cleaned)) / sr, audio_cleaned, 'g-', linewidth=0.5)
axes[1].set_title(f"После удаления тишины (длина: {len(audio_cleaned)/sr:.2f} с, удалено {100*(1-len(audio_cleaned)/len(data)):.1f}%)")
axes[1].set_xlabel("Время (секунды)")
axes[1].set_ylabel("Амплитуда")
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ===== СОХРАНЯЕМ РЕЗУЛЬТАТ =====
sf.write("audio_cleaned.wav", audio_cleaned, sr)
print(f"\nРезультат сохранен в: audio_cleaned.wav")