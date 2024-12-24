import numpy as np
import os
matrix = np.load("./2_task/second_task.npy")

x = []
y = []
z = []

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        if matrix[i][j] > 500 + 90:
            x.append(i)
            y.append(j)
            z.append(matrix[i][j])

np.savez("./2_task/second_task_result.npz", x = x, y = y, z = z)
np.savez_compressed("./2_task/second_task_compress_result.npz", x = x, y = y, z = z)

first_size = os.path.getsize('./2_task/second_task_result.npz')
second_size = os.path.getsize('./2_task/second_task_compress_result.npz')
print(f"savez = {first_size}")
print(f"savez_compressed = {second_size}")

print(f"diff = {first_size - second_size}")
#Сжатый файл примерно в 3 раза меньше