import pandas as pd
import os

# 1. 加载CSV文件
input_csv_path = r"F:\SEED-VIG数据集\1.滤波\1.csv"  # 输入文件路径
output_folder = r"F:\SEED-VIG数据集\2.分段\1"  # 输出文件夹路径

# 检查输出文件夹是否存在，不存在则创建
os.makedirs(output_folder, exist_ok=True)

# 加载 CSV 数据
eeg_data = pd.read_csv(input_csv_path, header=None)  # 无列名的CSV文件
eeg_data = eeg_data.values  # 转为NumPy数组，形状为 (1416000, 17)

# 2. 转置数据
eeg_data_transposed = eeg_data.T  # 转置后形状为 (17, 1416000)

# 3. 将数据分段并保存为单独的CSV文件
# 每段包含 17×1600 的数据
segment_length = 1600  # 每段时间点数
num_segments = eeg_data_transposed.shape[1] // segment_length  # 总段数 (1416000 / 1600 = 885)

for i in range(num_segments):
    # 提取当前段的数据
    segment_data = eeg_data_transposed[:, i * segment_length:(i + 1) * segment_length]  # 17×1600

    # 构造文件名
    segment_filename = os.path.join(output_folder, f"EEG{i + 1}.csv")

    # 将数据保存为CSV文件
    pd.DataFrame(segment_data).to_csv(segment_filename, index=False, header=False)
    print(f"保存段 {i + 1}/{num_segments} 到文件：{segment_filename}")

print(f"所有 {num_segments} 个段已保存到文件夹：{output_folder}")