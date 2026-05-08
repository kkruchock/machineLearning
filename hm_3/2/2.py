import pandas as pd

url = 'https://raw.githubusercontent.com/agconti/kaggle-titanic/master/data/train.csv'
data = pd.read_csv(url)

pclass_all = data['Pclass'].value_counts().sort_index()
print(pclass_all)
print()

males = data[data['Sex'] == 'male']
pclass_males = males['Pclass'].value_counts().sort_index()
print(pclass_males)
print()

females = data[data['Sex'] == 'female']
pclass_females = females['Pclass'].value_counts().sort_index()
print(pclass_females)
print()

print(pclass_males[2])