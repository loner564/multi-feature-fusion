import os
import numpy as np

def fill_zeros(matrix):
  copy_matrix = matrix.copy().astype(float)  # 将矩阵复制为浮点型
  rows, cols = matrix.shape

  for i in range(rows):
    for j in range(cols):
      if matrix[i, j] == 0:
        neighbors = []

        # 上
        if i > 0 and matrix[i-1, j] != 0:
          neighbors.append(matrix[i-1, j])

        # 下
        if i < rows - 1 and matrix[i+1, j] != 0:
          neighbors.append(matrix[i+1, j])

        # 左
        if j > 0 and matrix[i, j-1] != 0:
          neighbors.append(matrix[i, j-1])

        # 右
        if j < cols - 1 and matrix[i, j+1] != 0:
          neighbors.append(matrix[i, j+1])

        if neighbors:
          average = sum(neighbors) / len(neighbors)
          if average.is_integer():  # 检查是否是整数
            copy_matrix[i, j] = int(average)  # 转换为整数
          else:
            copy_matrix[i, j] = average  # 保留小数

  return copy_matrix

# 大文件夹路径
folder_path = "F:/SEED-VIG数据集/19.归一化/1"

# 新的大文件夹路径
new_folder_path = "F:/SEED-VIG数据集/20.数据填充/1"

# 遍历大文件夹下的子文件夹
for sub_folder in os.listdir(folder_path):
  sub_folder_path = os.path.join(folder_path, sub_folder)

  # 确保是文件夹
  if os.path.isdir(sub_folder_path):
    # 新的子文件夹路径
    new_sub_folder_path = os.path.join(new_folder_path, sub_folder)
    os.makedirs(new_sub_folder_path, exist_ok=True)  # 创建新的子文件夹

    # 遍历子文件夹下的CSV文件
    for file_name in os.listdir(sub_folder_path):
      file_path = os.path.join(sub_folder_path, file_name)

      # 确保是CSV文件
      if file_name.endswith('.csv'):
        # 读取原始CSV文件
        original_matrix = np.loadtxt(file_path, delimiter=',')

        # 调用填充函数
        result_matrix = fill_zeros(original_matrix)

        # 将结果转换为浮点型数据
        result_matrix = result_matrix.astype(float)

        # 设置精度为6位小数，避免科学计数法
        np.set_printoptions(precision=6, suppress=True)

        # 新的CSV文件路径
        new_file_path = os.path.join(new_sub_folder_path, file_name)

        # 将结果保存为新的CSV文件
        np.savetxt(new_file_path, result_matrix, delimiter=',', fmt='%0.6f')
