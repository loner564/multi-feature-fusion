import os
import pandas as pd
import numpy as np

# 主目录
root_dir = r'F:\SEED-VIG数据集\7.网络归一化\1'
# 输出目录
output_dir = r'F:\SEED-VIG数据集\8.阈值选择\1'

# 遍历主目录下的子文件夹
for sub_dir in os.listdir(root_dir):
    sub_path = os.path.join(root_dir, sub_dir)
    if not os.path.isdir(sub_path):  # 如果不是文件夹则跳过
        continue

    # 初始化总和和计数器
    total_sum = 0
    data_count = 0
    file_paths = []

    # 获取子文件夹中所有Excel文件路径
    for root, dirs, files in os.walk(sub_path):
        for file in files:
            if file.endswith('.xlsx') or file.endswith('.xls'):
                file_path = os.path.join(root, file)
                file_paths.append(file_path)

    # 计算当前子文件夹的平均值（忽略对角线）
    for file_path in file_paths:
        df = pd.read_excel(file_path, index_col=None, header=None)
        matrix = df.values  # 转换为numpy矩阵
        mask = np.ones(matrix.shape, dtype=bool)  # 创建布尔掩码
        np.fill_diagonal(mask, False)  # 将对角线位置设置为False，表示忽略
        total_sum += matrix[mask].sum()  # 仅统计非对角线元素的总和
        data_count += mask.sum()  # 仅统计非对角线元素的个数

    # 计算平均值
    average_value = total_sum / data_count

    # 修改数据并根据条件赋值
    for file_path in file_paths:
        df = pd.read_excel(file_path, index_col=None, header=None)
        matrix = df.values  # 转换为numpy矩阵
        mask = np.ones(matrix.shape, dtype=bool)  # 创建布尔掩码
        np.fill_diagonal(mask, False)  # 将对角线位置设置为False

        # 修改矩阵：对非对角线元素应用阈值操作
        matrix[mask] = np.where(matrix[mask] < average_value, 0, matrix[mask])

        # 生成新的保存路径
        relative_path = os.path.relpath(file_path, root_dir)  # 获取文件的相对路径
        new_file_path = os.path.join(output_dir, relative_path)
        os.makedirs(os.path.dirname(new_file_path), exist_ok=True)  # 创建目标文件夹
        pd.DataFrame(matrix).to_excel(new_file_path, index=False, header=False)

    # 输出当前子文件夹的平均值
    print(f"子文件夹 '{sub_dir}' 的平均值: {average_value}")

print("处理完成.")