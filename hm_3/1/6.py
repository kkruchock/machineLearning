import pandas as pd

url = 'https://raw.githubusercontent.com/new-okaerinasai/math-ml-hse-2019/master/sem01_intro/math_students.csv'
data = pd.read_csv(url)

# частота значений внеклассных активностей
activities_counts = data['activities'].value_counts()
print(activities_counts)
# самое поплуряное
most_common_activities = activities_counts.index[0]
print(most_common_activities)

# студенты имеющие эту активность
filtered_students = data[data['activities'] == most_common_activities]
print(filtered_students)

# распределение по кол-ву пропусков
absences_counts = filtered_students['absences'].value_counts()
print(absences_counts)

# значение пропусков с наибольшим количеством студентов
print("answer", absences_counts.index[0])

