import pandas as pd

url = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv'
data = pd.read_csv(url)

clean_data = data.dropna(subset=['Age'])

age_by_sex_class = clean_data.groupby(['Sex', 'Pclass'])['Age'].mean().round(1)

print("СРЕДНИЙ ВОЗРАСТ ПО ПОЛУ И КЛАССУ")
print(age_by_sex_class)
print()

pivot_table = clean_data.pivot_table(values='Age', index='Sex', columns='Pclass', aggfunc='mean').round(1)
print(pivot_table)