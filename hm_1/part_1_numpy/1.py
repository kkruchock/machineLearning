import numpy as np

arr = np.random.randint(1, 101, size = 100) # np.random.uniform для не целых
avg = np.mean(arr)

print("массив до замены:")
print(arr)

def is_prime(n):
  if n < 2:
    return False
  for i in range(2, int(np.sqrt(n)) + 1):
    if n % i == 0:
      return False
  return True

for i in range(len(arr)):
  if arr[i] > avg and is_prime(arr[i]):
    arr[i] = 0

print("массив после замены:")
print(arr)