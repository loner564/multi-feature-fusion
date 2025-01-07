import os
import pandas as pd

# 定义原始文件夹路径
folder_path = "F:/SEED-VIG数据集/18.映射/1"

# 定义归一化后文件夹路径
normalized_folder_path = "F:/SEED-VIG数据集/19.归一化/1"

# 创建归一化后文件夹路径
os.makedirs(normalized_folder_path, exist_ok=True)

# 定义子文件夹名称列表
subfolders = ["1", "2", "3"]

# 遍历子文件夹
for subfolder in subfolders:
    subfolder_path = os.path.join(folder_path, subfolder)

    # 创建归一化后子文件夹路径
    normalized_subfolder_path = os.path.join(normalized_folder_path, subfolder)
    os.makedirs(normalized_subfolder_path, exist_ok=True)

    # 定义变量来保存最大值和最小值
    max_value = float('-inf')
    min_value = float('inf')

    # 遍历文件夹和子文件夹
    for root, dirs, files in os.walk(subfolder_path):
        for file in files:
            # 筛选CSV文件
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                # 读取CSV文件
                df = pd.read_csv(file_path, header=None)
                # 将数据转换为数字类型
                data = df.astype(float)
                # 更新最大值和最小值
                file_max = data.max().max()
                file_min = data.min().min()
                if file_max > max_value:
                    max_value = file_max
                    # if max_value == 3069.198745:
                    #     print(file_path)

                if file_min < min_value:
                    min_value = file_min

    print(f"{subfolder} max value: {max_value}")
    print(f"{subfolder} min value: {min_value}")

    # 再次遍历文件夹和子文件夹，进行归一化处理并保存到新路径
    for root, dirs, files in os.walk(subfolder_path):
        for file in files:
            # 筛选CSV文件
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                # 读取CSV文件
                df = pd.read_csv(file_path, header=None)
                # 将数据转换为数字类型
                data = df.astype(float)
                # 归一化处理
                normalized_data = (data - min_value) / (max_value - min_value)
                # 获取原始文件夹子文件夹名称
                original_subfolder = os.path.basename(subfolder_path)
                original_file_path = os.path.join(original_subfolder, file)
                # 保存归一化后的数据到新的CSV文件
                normalized_file_path = os.path.join(normalized_subfolder_path, file)
                normalized_data.to_csv(normalized_file_path, index=False, header=False)

    # # 重置最大值和最小值
    # max_value = float('-inf')
    # min_value = float('inf')
