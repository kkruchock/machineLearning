# ответ - 17
import pandas as pd

url = 'https://raw.githubusercontent.com/new-okaerinasai/math-ml-hse-2019/master/sem01_intro/math_students.csv'
data = pd.read_csv(url)

# фильтруем студентов школы MS
ms_students = data[data['school'] == 'MS']

# находим минимальный возраст
print(ms_students['age'].min())
