import os
import pandas as pd
import pywt
import numpy as np

# 定义路径
input_dir = r"F:\SEED-VIG数据集\3.分类\1\3"  # 原始CSV文件夹路径
output_dir = r"F:\SEED-VIG数据集\4.小波分解\1\3"  # 小波分解结果保存路径
os.makedirs(output_dir, exist_ok=True)

# 创建五个频段子文件夹
bands = {
    "1-4Hz": "1_4Hz",
    "4-8Hz": "4_8Hz",
    "8-14Hz": "8_14Hz",
    "14-31Hz": "14_31Hz",
    "31-50Hz": "31_50Hz"
}

for band in bands.values():
    os.makedirs(os.path.join(output_dir, band), exist_ok=True)

# 定义小波分解函数
def wavelet_decomposition(data, fs=1000):
    """
    对信号进行小波分解并提取不同频段
    :param data: 输入信号 (1D数组)
    :param fs: 采样频率
    :return: 各频段信号字典
    """
    wavelet = "db4"  # 小波基
    coeffs = pywt.wavedec(data, wavelet, level=6)  # 小波分解6层

    # 频段映射到小波系数
    bands_data = {
        "1-4Hz": coeffs[-1],  # 第6层
        "4-8Hz": coeffs[-2],  # 第5层
        "8-14Hz": coeffs[-3],  # 第4层
        "14-31Hz": coeffs[-4],  # 第3层
        "31-50Hz": coeffs[-5]  # 第2层
    }

    return bands_data

# 处理文件
for file_name in os.listdir(input_dir):
    if file_name.endswith(".csv"):
        # 读取CSV文件
        file_path = os.path.join(input_dir, file_name)
        data = pd.read_csv(file_path, header=None, index_col=0)  # 保留通道名作为索引

        # 小波分解
        for band, band_folder in bands.items():
            band_data = []  # 存储每个通道的分解结果
            for channel in data.index:
                channel_data = data.loc[channel].values  # 获取通道信号
                decomposed_data = wavelet_decomposition(channel_data)  # 分解
                band_data.append(decomposed_data[band])  # 提取目标频段

            # 保存结果
            band_df = pd.DataFrame(band_data, index=data.index)  # 以通道名为索引
            output_file = os.path.join(output_dir, band_folder, file_name)
            band_df.to_csv(output_file, index=True, header=False)
            print(f"已保存文件: {output_file}")

print("所有文件的小波分解已完成并保存。")