import os
import pandas as pd
import numpy as np

# 读取矩阵
matrix = np.array([
    ['FT7', 0, 0, 0, 0, 0, 0, 0, 'FT8'],
    ['T7', 0, 0, 0, 0, 0, 0, 0, 'T8'],
    ['TP7', 0, 0, 'CP1', 0, 'CP2', 0, 0, 'TP8'],
    [0, 0, 0, 'P1', 0, 'P2', 0, 0, 0],
    [0, 0, 0, 'PO3', 0, 'PO4', 0, 0, 0],
    [0, 0, 0, 'O1', 0, 'O2', 0, 0, 0]
])

# 创建映射字典
channel_map = {}
for row in range(matrix.shape[0]):
    for col in range(matrix.shape[1]):
        if matrix[row, col] is not None:
            channel_map[matrix[row, col]] = (row, col)

# 设置大文件夹路径和新大文件夹路径
folder_path = "F:/SEED-VIG数据集/17.加通道列/1"
new_folder_path = "F:/SEED-VIG数据集/18.映射/1"
os.makedirs(new_folder_path, exist_ok=True)

# 遍历大文件夹中的子文件夹
for sub_folder in ['1', '2', '3']:
    # 子文件夹路径
    sub_folder_path = os.path.join(folder_path, sub_folder)
    # 新子文件夹路径
    new_sub_folder_path = os.path.join(new_folder_path, sub_folder)
    os.makedirs(new_sub_folder_path, exist_ok=True)

    # 遍历子文件夹中的CSV文件
    for filename in os.listdir(sub_folder_path):
        if filename.endswith(".csv"):
            # 构建文件路径
            file_path = os.path.join(sub_folder_path, filename)
            # 读取CSV文件
            data_csv = pd.read_csv(file_path)
            # 映射数据到矩阵
            mapped_data = []
            for channel_name in data_csv['channels']:
                if channel_name in channel_map:
                    row, col = channel_map[channel_name]
                    data_value = data_csv.loc[data_csv['channels'] == channel_name, 'SQ'].iloc[0]
                    mapped_data.append((row, col, data_value))
            # 在矩阵对应位置填充数据
            for item in mapped_data:
                row, col, data_value = item
                matrix[row, col] = data_value
            # 创建填充后的数据框
            df = pd.DataFrame(matrix)
            # 构建结果文件路径
            output_file = os.path.join(new_sub_folder_path, f"{filename}")
            # 保存数据框为CSV文件，不包含行索引
            df.to_csv(output_file, index=False, header=False)