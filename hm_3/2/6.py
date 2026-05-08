import pandas as pd

data = pd.read_csv('https://raw.githubusercontent.com/agconti/kaggle-titanic/master/data/train.csv')
men = data[data['Sex'] == 'male']

men['first_name'] = men['Name'].str.split(',').str[1].str.split().str[1]
print(men['first_name'].value_counts().index[0])