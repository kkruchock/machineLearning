import pandas as pd

url = 'https://raw.githubusercontent.com/agconti/kaggle-titanic/master/data/train.csv'
data = pd.read_csv(url)

gender_counts = data['Sex'].value_counts()

print(gender_counts)