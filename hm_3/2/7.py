import pandas as pd
import matplotlib.pyplot as plt

url = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv'
data = pd.read_csv(url)

clean_data = data.dropna(subset=['Age'])

survived = clean_data[clean_data['Survived'] == 1]
died = clean_data[clean_data['Survived'] == 0]

print(f"Выживших (с известным возрастом): {len(survived)}")
print(f"Погибших (с известным возрастом): {len(died)}")
print()
# распределение стоимости
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Выжившие
axes[0].hist(survived['Fare'], bins=30, color='green', alpha=0.7, edgecolor='black')
axes[0].axvline(survived['Fare'].mean(), color='darkgreen', linestyle='--', linewidth=2,
                label=f'Среднее: {survived["Fare"].mean():.2f}')
axes[0].axvline(survived['Fare'].median(), color='lightgreen', linestyle=':', linewidth=2,
                label=f'Медиана: {survived["Fare"].median():.2f}')
axes[0].set_xlabel('Стоимость билета (Fare)')
axes[0].set_ylabel('Количество пассажиров')
axes[0].set_title('ВЫЖИВШИЕ')
axes[0].legend()

# Погибшие
axes[1].hist(died['Fare'], bins=30, color='red', alpha=0.7, edgecolor='black')
axes[1].axvline(died['Fare'].mean(), color='darkred', linestyle='--', linewidth=2,
                label=f'Среднее: {died["Fare"].mean():.2f}')
axes[1].axvline(died['Fare'].median(), color='lightcoral', linestyle=':', linewidth=2,
                label=f'Медиана: {died["Fare"].median():.2f}')
axes[1].set_xlabel('Стоимость билета (Fare)')
axes[1].set_ylabel('Количество пассажиров')
axes[1].set_title('ПОГИБШИЕ')
axes[1].legend()

plt.suptitle('Распределение стоимости билетов', fontsize=14)
plt.tight_layout()
plt.show()

# распределение возраста
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Выжившие
axes[0].hist(survived['Age'], bins=30, color='green', alpha=0.7, edgecolor='black')
axes[0].axvline(survived['Age'].mean(), color='darkgreen', linestyle='--', linewidth=2,
                label=f'Среднее: {survived["Age"].mean():.2f}')
axes[0].axvline(survived['Age'].median(), color='lightgreen', linestyle=':', linewidth=2,
                label=f'Медиана: {survived["Age"].median():.2f}')
axes[0].set_xlabel('Возраст')
axes[0].set_ylabel('Количество пассажиров')
axes[0].set_title('ВЫЖИВШИЕ')
axes[0].legend()

# Погибшие
axes[1].hist(died['Age'], bins=30, color='red', alpha=0.7, edgecolor='black')
axes[1].axvline(died['Age'].mean(), color='darkred', linestyle='--', linewidth=2,
                label=f'Среднее: {died["Age"].mean():.2f}')
axes[1].axvline(died['Age'].median(), color='lightcoral', linestyle=':', linewidth=2,
                label=f'Медиана: {died["Age"].median():.2f}')
axes[1].set_xlabel('Возраст')
axes[1].set_ylabel('Количество пассажиров')
axes[1].set_title('ПОГИБШИЕ')
axes[1].legend()

plt.suptitle('Распределение возраста', fontsize=14)
plt.tight_layout()
plt.show()

print(f"Средний возраст ВЫЖИВШИХ: {survived['Age'].mean():.2f} лет")
print(f"Средний возраст ПОГИБШИХ: {died['Age'].mean():.2f} лет")
print()

if died['Age'].mean() > survived['Age'].mean():
    print("✅ ВЕРНО: Средний возраст погибших ВЫШЕ, чем выживших.")
else:
    print("❌ НЕВЕРНО: Средний возраст выживших выше или равен среднему возрасту погибших.")