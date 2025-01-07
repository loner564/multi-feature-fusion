import os
import pandas as pd

# 定义文件夹路径
network_normalization_dir = 'F:/SEED-VIG数据集/8.阈值选择/1'
symmetric_entropy_dir = 'F:/SEED-VIG数据集/21.拼接对称商微分熵/1'
output_dir = 'F:/SEED-VIG数据集/22.三特征融合/1'

# 确保输出文件夹存在
os.makedirs(output_dir, exist_ok=True)

# 处理每个子文件夹
for subfolder in ['1', '2', '3']:
  network_folder = os.path.join(network_normalization_dir, subfolder)
  entropy_folder = os.path.join(symmetric_entropy_dir, subfolder)
  output_subfolder = os.path.join(output_dir, subfolder)
  os.makedirs(output_subfolder, exist_ok=True)

  # 获取所有Excel文件
  network_files = [f for f in os.listdir(network_folder) if f.endswith('.xlsx')]
  for file in network_files:
    # 读取Excel文件
    network_data = pd.read_excel(os.path.join(network_folder, file), header=None)
    file_number = file.split('EEG')[-1].split('.')[0]  # 提取文件编号

    # 查找对应的CSV文件
    entropy_file = f'merged_{file_number}.csv'
    if entropy_file in os.listdir(entropy_folder):
      entropy_data = pd.read_csv(os.path.join(entropy_folder, entropy_file), header=None)

      # 合并数据并保存
      merged_data = pd.concat([network_data, entropy_data], ignore_index=True)
      merged_data.to_csv(os.path.join(output_subfolder, f'merged_{file_number}.csv'), index=False, header=False)