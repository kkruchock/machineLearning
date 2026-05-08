# ответ - 1.26 (в отношениях оценки хуже)
import pandas as pd

url = 'https://raw.githubusercontent.com/new-okaerinasai/math-ml-hse-2019/master/sem01_intro/math_students.csv'
data = pd.read_csv(url)

# средняя оценка студентов, состоящих в отношениях
romantic_yes = data[data['romantic'] == 'yes']['G3'].mean()

# аналагично
romantic_no = data[data['romantic'] == 'no']['G3'].mean()

print(abs(round(romantic_yes - romantic_no, 2)))

