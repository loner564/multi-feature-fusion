import os
import pandas as pd

# 定义通道列表
channels = ['FT7', 'FT8', 'T7', 'T8', 'TP7', 'TP8', 'CP1', 'CP2', 'P1', 'PZ', 'P2', 'PO3', 'POZ', 'PO4', 'O1', 'OZ', 'O2']

# 大文件夹路径
folder_path = "F:/SEED-VIG数据集/9.提取DE/1"
# 新大文件夹路径
new_folder_path = "F:/SEED-VIG数据集/10.加通道列/1"

# 创建新大文件夹
os.makedirs(new_folder_path, exist_ok=True)

# 遍历大文件夹中的子文件夹
for sub_folder in ['1-4', '4-8', '8-14', '14-31', '31-50']:
    # 子文件夹路径
    sub_folder_path = os.path.join(folder_path, sub_folder)
    # 新子文件夹路径
    new_sub_folder_path = os.path.join(new_folder_path, sub_folder)

    # 创建新子文件夹
    os.makedirs(new_sub_folder_path, exist_ok=True)

    # 遍历子文件夹中的CSV文件
    for file_name in os.listdir(sub_folder_path):
        if file_name.endswith('.csv'):
            # CSV文件路径
            file_path = os.path.join(sub_folder_path, file_name)

            # 读取CSV文件
            df = pd.read_csv(file_path)

            # 添加新列
            df['channels'] = channels

            # 保存修改后的CSV文件到新子文件夹
            output_file_path = os.path.join(new_sub_folder_path, file_name)
            df.to_csv(output_file_path, index=False)
