import os
import numpy as np
import pandas as pd

# 定义输入和输出路径
input_dir = r'F:\SEED-VIG数据集\4.小波分解\1\3\14_31Hz'
output_dir = r'F:\SEED-VIG数据集\15.提14通道\1\3'

# 如果输出路径不存在，则创建
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 遍历输入目录及其子目录
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith('.csv'):  # 只处理 CSV 文件
            # 构建文件路径
            file_path = os.path.join(root, file)

            # 读取 CSV 文件
            data = pd.read_csv(file_path, header=None)  # 不带列名
            # 删除第一列（通道列）和第10, 13, 16行（Python索引从0开始）
            data_modified = data.drop(columns=[0], axis=1)  # 删除第一列
            data_modified = data_modified.drop(index=[9, 12, 15], axis=0)  # 删除指定行

            # 生成对应的输出路径
            relative_path = os.path.relpath(file_path, input_dir)  # 获取相对路径
            output_file_path = os.path.join(output_dir, relative_path)  # 构建输出文件路径

            # 确保输出文件夹存在
            output_folder = os.path.dirname(output_file_path)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # 保存修改后的数据为 CSV 文件
            data_modified.to_csv(output_file_path, index=False, header=False)  # 不保存索引和列名
            print(f"已处理并保存文件: {output_file_path}")

print("所有文件已处理完成！")