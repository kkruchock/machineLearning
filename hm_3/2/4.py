import pandas as pd

url = 'https://raw.githubusercontent.com/agconti/kaggle-titanic/master/data/train.csv'
data = pd.read_csv(url)

# убираем строки с пропущенным возрастом
clean_data = data.dropna(subset=['Age'])

young = clean_data[clean_data['Age'] < 30]
young_total = len(young)
young_survived = young['Survived'].sum()  # 1 = выжил
young_survival_rate = young_survived / young_total

old = clean_data[clean_data['Age'] > 60]
old_total = len(old)
old_survived = old['Survived'].sum()
old_survival_rate = old_survived / old_total

print(f"Пассажиры младше 30 лет:")
print(f"  - Всего: {young_total}")
print(f"  - Выжило: {young_survived}")
print(f"  - Доля выживших: {young_survival_rate:.2%}")
print()
print(f"Пассажиры старше 60 лет:")
print(f"  - Всего: {old_total}")
print(f"  - Выжило: {old_survived}")
print(f"  - Доля выживших: {old_survival_rate:.2%}")

if young_survival_rate > old_survival_rate:
    print(f"✅ Правда. Люди моложе 30 лет выживали чаще.")
    print(f"   ({young_survival_rate:.2%} vs {old_survival_rate:.2%})")
else:
    print(f"❌ Неправда. Люди старше 60 лет выживали чаще.")
    print(f"   ({old_survival_rate:.2%} vs {young_survival_rate:.2%})")