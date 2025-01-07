import os
import pandas as pd
import numpy as np

def normalize_matrix_with_zero_diagonal(matrix):
    # 复制矩阵
    normalized_matrix = matrix.copy()
    # 提取并处理非对角线元素
    flat_matrix = matrix.flatten()
    diagonal_indices = np.arange(0, len(flat_matrix), matrix.shape[1] + 1)
    non_diagonal_elements = np.delete(flat_matrix, diagonal_indices)
    # 计算最小值和最大值
    min_value = non_diagonal_elements.min()
    max_value = non_diagonal_elements.max()
    # 归一化非对角线元素
    for i in range(normalized_matrix.shape[0]):
        for j in range(normalized_matrix.shape[1]):
            if i != j:  # 跳过对角线元素
                normalized_matrix[i, j] = (matrix[i, j] - min_value) / (max_value - min_value)
    return normalized_matrix

# 源文件夹路径
source_folder = "F:/SEED-VIG数据集/6.相对小波熵复杂网络/1"
# 目标文件夹路径
target_folder = "F:/SEED-VIG数据集/7.网络归一化/1"

# 遍历源文件夹中的所有子文件夹
for subdir in os.listdir(source_folder):
    subdir_path = os.path.join(source_folder, subdir)
    # 检查是否为子文件夹
    if os.path.isdir(subdir_path):
        for file in os.listdir(subdir_path):
            if file.endswith(".csv"):
                # 处理每个CSV文件
                file_path = os.path.join(subdir_path, file)
                csv_data = pd.read_csv(file_path, header=None)
                # 归一化处理
                normalized_matrix = normalize_matrix_with_zero_diagonal(csv_data.to_numpy())
                # 保存归一化后的数据到目标文件夹
                target_subdir = os.path.join(target_folder, subdir)
                if not os.path.exists(target_subdir):
                    os.makedirs(target_subdir)
                target_file_path = os.path.join(target_subdir, file.replace(".csv", ".xlsx"))
                pd.DataFrame(normalized_matrix).to_excel(target_file_path, index=False, header=False)