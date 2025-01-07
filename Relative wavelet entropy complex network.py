import os
import pandas as pd
import numpy as np

# 相关性计算函数
def calculate_correlation(data):
    """
    计算相关性矩阵
    :param data: 输入数据 (二维 numpy 数组)
    :return: 相关性矩阵 (二维 numpy 数组)
    """
    n, m = data.shape
    result = np.zeros((n, n))
    for i in range(n):
        extract_data = data[i, :]
        for j in range(n):
            extract_data0 = data[j, :]
            sum_value = 0
            for k in range(m):
                if extract_data[k] > 0 and extract_data0[k] > 0:  # 避免 log(0) 的情况
                    sum_value += extract_data[k] * np.log(extract_data[k] / extract_data0[k])
            result[i, j] = sum_value
    return result

if __name__ == '__main__':
    # 原始数据文件夹
    source_dir = r"F:\SEED-VIG数据集\5.相对小波能量\1"
    # 结果数据保存文件夹
    target_dir = r"F:\SEED-VIG数据集\6.相对小波熵复杂网络\1"

    # 遍历所有子文件夹及文件
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".csv"):  # 只处理 CSV 文件
                # 构建完整文件路径
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, source_dir)  # 相对路径
                target_file_path = os.path.join(target_dir, relative_path)  # 保持目录结构

                # 读取数据（跳过第一行标签行）
                df = pd.read_csv(file_path, header=0)  # header=0 表示第一行为列名

                # 确保数据为数值类型，并处理空值
                df = df.apply(pd.to_numeric, errors='coerce').fillna(0)  # 转换为数值并用 0 填充空值
                data = df.values

                # 计算相关性矩阵
                result = calculate_correlation(data)

                # 构建目标文件目录
                target_folder = os.path.dirname(target_file_path)
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)

                # 保存结果为 CSV 文件
                result_df = pd.DataFrame(result)
                result_df.to_csv(target_file_path, index=False, header=False)  # 不保存索引和列名
                print(f"已处理并保存文件: {target_file_path}")

    print("所有文件已处理完成！")