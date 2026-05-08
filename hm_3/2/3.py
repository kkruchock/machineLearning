import pandas as pd

url = 'https://raw.githubusercontent.com/agconti/kaggle-titanic/master/data/train.csv'
data = pd.read_csv(url)

median_fare = round(data['Fare'].median(), 2)

std_fare = round(data['Fare'].std(), 2)

print(f"Медиана стоимости билета: {median_fare}")
print(f"Стандартное отклонение стоимости билета: {std_fare}")