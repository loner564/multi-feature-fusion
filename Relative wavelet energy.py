import os
import pandas as pd
import pywt
import numpy as np

# 定义路径
input_dir = r"F:\SEED-VIG数据集\3.分类\1\3"  # 原始CSV文件夹路径
output_dir = r"F:\SEED-VIG数据集\5.相对小波能量\1\3"  # 相对小波能量结果保存路径
os.makedirs(output_dir, exist_ok=True)  # 如果文件夹不存在，则创建

# 定义小波分解函数
def wavelet_decomposition(data, wavelet="db4", level=6):
    """
    对信号进行小波分解并返回所有分解系数
    :param data: 输入信号 (1D数组)
    :param wavelet: 小波基
    :param level: 分解层数
    :return: 分解系数列表
    """
    coeffs = pywt.wavedec(data, wavelet, level=level)  # 小波分解
    return coeffs

# 定义计算相对小波能量的函数
def compute_relative_wavelet_energy(data, wavelet="db4", level=6):
    """
    计算信号的相对小波能量
    :param data: 输入信号 (1D数组)
    :param wavelet: 小波基
    :param level: 分解层数
    :return: 各频段的相对能量值列表
    """
    # 处理信号为空或全零的情况
    if np.all(data == 0):
        return [0] * 5  # 返回零能量

    coeffs = wavelet_decomposition(data, wavelet, level)

    # 如果分解层数不足，补全到 5 层
    if len(coeffs) < 5:
        coeffs = coeffs + [np.zeros_like(coeffs[-1])] * (5 - len(coeffs))

    total_energy = sum(np.sum(np.square(c)) for c in coeffs)  # 总能量
    if total_energy == 0:  # 防止总能量为 0 的情况
        return [0] * 5

    relative_energy = [np.sum(np.square(c)) / total_energy for c in coeffs[:5]]  # 相对能量（前5层）
    return relative_energy

# 定义处理文件的主逻辑
for file_name in os.listdir(input_dir):
    if file_name.endswith(".csv"):
        # 读取CSV文件
        file_path = os.path.join(input_dir, file_name)
        data = pd.read_csv(file_path, header=None, index_col=0)  # 保留通道名作为索引

        # 存储每个通道的相对能量
        relative_energy_all_channels = []

        for channel in data.index:
            channel_data = data.loc[channel].values  # 获取通道信号
            relative_energy = compute_relative_wavelet_energy(channel_data)  # 计算相对能量
            relative_energy_all_channels.append(relative_energy)

        # 将结果保存为DataFrame (18行×5列)
        columns = ["1-4Hz", "4-8Hz", "8-14Hz", "14-31Hz", "31-50Hz"]
        result_df = pd.DataFrame(relative_energy_all_channels, columns=columns)

        # 保存到输出文件夹（不保存通道列）
        output_file = os.path.join(output_dir, file_name)
        result_df.to_csv(output_file, index=False, header=True)
        print(f"已保存文件: {output_file}")

print("所有文件的相对小波能量已计算并保存（不含通道列）。")