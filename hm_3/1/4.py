# ответ - 41
import pandas as pd

url = 'https://raw.githubusercontent.com/new-okaerinasai/math-ml-hse-2019/master/sem01_intro/math_students.csv'
data = pd.read_csv(url)

# оставляем только с нечетными пропусками
odd_absences = data[data['absences'] % 2 == 1]

# считаем количество
print(len(odd_absences))