import pandas as pd

url = 'https://raw.githubusercontent.com/agconti/kaggle-titanic/master/data/train.csv'
data = pd.read_csv(url)

women = data[data['Sex'] == 'female']
women_total = len(women)
women_survived = women['Survived'].sum()
women_survival_rate = women_survived / women_total

men = data[data['Sex'] == 'male']
men_total = len(men)
men_survived = men['Survived'].sum()
men_survival_rate = men_survived / men_total

print(f"Женщины:")
print(f"  - Всего: {women_total}")
print(f"  - Выжило: {women_survived}")
print(f"  - Доля выживших: {women_survival_rate:.2%}")
print()
print(f"Мужчины:")
print(f"  - Всего: {men_total}")
print(f"  - Выжило: {men_survived}")
print(f"  - Доля выживших: {men_survival_rate:.2%}")
print()

if women_survival_rate > men_survival_rate:
    print(f"✅ Правда. Женщины выживали чаще мужчин.")
    print(f"   ({women_survival_rate:.2%} vs {men_survival_rate:.2%})")
else:
    print(f"❌ Неправда. Мужчины выживали чаще женщин.")
    print(f"   ({men_survival_rate:.2%} vs {women_survival_rate:.2%})")