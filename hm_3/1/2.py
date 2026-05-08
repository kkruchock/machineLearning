# ответ - 0
import pandas as pd

url = 'https://raw.githubusercontent.com/new-okaerinasai/math-ml-hse-2019/master/sem01_intro/math_students.csv'
data = pd.read_csv(url)

# фильтруем строки, где и у отца и у матери нет образования
no_education = data[(data['Medu'] == 0) & (data['Fedu'] == 0)]

# и считаем их
print(len(no_education))
