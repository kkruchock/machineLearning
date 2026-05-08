import re
from collections import Counter
import matplotlib.pyplot as plt

# вместо !wget
import requests

url = "https://www.lib.ru/LITRA/PUSHKIN/saltan.txt"
response = requests.get(url)
response.encoding = "koi8-r"
text = response.text

def clean_text(text):
    # Приводим к нижнему регистру и заменяем ё на е
    text = text.lower().replace('ё', 'е')

    # Оставляем только русские буквы, пробелы и переводы строк
    # Всё остальное заменяем на пробел
    text = ''.join([c if c in ' абвгдежзийклмнопрстуфхцчшщъыьэюя\n' else ' ' for c in text])

    # Убираем лишние пробелы
    text = re.sub(' +', ' ', text)

    return text


text = clean_text(text)

# ================================================
# ЧАСТЬ 3: РАЗБИВАЕМ НА СТРОКИ И БЕРЕМ ПЕРВЫЕ 30 НЕПУСТЫХ
# ================================================

# Разбиваем текст на строки
all_lines = text.split('\n')

# Берем только непустые строки (игнорируем пустые)
non_empty_lines = [line.strip() for line in all_lines if line.strip()]

# Берем первые 31 непустых строк
lines = non_empty_lines[:31]

print(f"Всего в тексте строк: {len(all_lines)}")
print(f"Непустых строк: {len(non_empty_lines)}")
print(f"Берем для анализа: {len(lines)} строк")
print()

print("=" * 50)
print("ВЗЯТЫЕ СТРОКИ (первые 31 непустых):")
print("=" * 50)
for i, line in enumerate(lines, 1):
    word_count = len(line.split())
    print(f"{i:2}. [{word_count:2} слов] {line[:60]}{'...' if len(line) > 60 else ''}")
print()

# общее кол-во слов в тексте

all_words = []
for line in lines:
    words = line.split()
    all_words.extend(words)

total_words = len(all_words)
print(f"1. Общее количество слов во всем тексте (31 строк): {total_words}")

# самая длинная и самая корткая

word_counts = [len(line.split()) for line in lines]

max_words = max(word_counts)
min_words = min(word_counts)

max_index = word_counts.index(max_words)
min_index = word_counts.index(min_words)

print(f"\n2. Самая длинная строка: {max_words} слов")
print(f"   \"{lines[max_index][:80]}{'...' if len(lines[max_index]) > 80 else ''}\"")
print(f"\n   Самая короткая строка: {min_words} {'слово' if min_words == 1 else 'слова' if min_words < 5 else 'слов'}")
print(f"   \"{lines[min_index]}\"")

# ================================================
# ЗАДАНИЕ 3: Гистограмма распределения длины строк (в словах)
# ================================================

unique_lengths = sorted(set(word_counts))
counts = [word_counts.count(l) for l in unique_lengths]

# Рисуем столбчатую диаграмму (категории на оси X)
plt.figure(figsize=(12, 6))
bars = plt.bar(unique_lengths, counts, width=0.6, edgecolor='black', alpha=0.7, color='skyblue')

# Подписываем значения над столбцами
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{int(height)}', ha='center', va='bottom', fontsize=11)

# Настройка осей
plt.xlabel('Количество слов в строке', fontsize=12)
plt.ylabel('Количество строк', fontsize=12)
plt.title('Распределение длины строк (в словах)', fontsize=14)

# Чтобы столбцы не сливались — делаем целые значения на оси X
plt.xticks(unique_lengths, [f"{l} слов" for l in unique_lengths], fontsize=10)

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# ================================================
# ЗАДАНИЕ 4: Топ-10 самых часто встречающихся слов
# ================================================

# Убираем короткие слова? Можно убрать, но задание не просит
word_counter = Counter(all_words)
top_words = word_counter.most_common(10)

print("\n4. Топ-10 самых часто встречающихся слов:")
print("-" * 30)
for i, (word, count) in enumerate(top_words, 1):
    print(f"{i:2}. \"{word}\" — {count} раз")

# Дополнительно: визуализация топ-10
plt.figure(figsize=(10, 5))
words = [w for w, _ in top_words]
counts = [c for _, c in top_words]
plt.bar(words, counts, color='lightcoral', edgecolor='black')
plt.xlabel('Слова')
plt.ylabel('Частота')
plt.title('Топ-10 самых часто встречающихся слов')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()