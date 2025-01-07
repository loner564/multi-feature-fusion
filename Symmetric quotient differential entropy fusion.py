import os
import pandas as pd
import re


def merge_and_save_csv_files(base_path_1, base_path_2, output_base_path):
    for subfolder in ['1', '2', '3']:
        path_1 = os.path.join(base_path_1, subfolder)
        path_2 = os.path.join(base_path_2, subfolder)
        output_path = os.path.join(output_base_path, subfolder)

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        def extract_number(file_name):
            match = re.search(r'\d+', file_name)
            return int(match.group()) if match else None

        files_1 = {extract_number(file): file for file in os.listdir(path_1)}
        files_2 = {extract_number(file): file for file in os.listdir(path_2)}

        common_numbers = set(files_1.keys()) & set(files_2.keys())

        for num in common_numbers:
            file_1 = files_1[num]
            file_2 = files_2[num]

            file_path_1 = os.path.join(path_1, file_1)
            file_path_2 = os.path.join(path_2, file_2)

            df1 = pd.read_csv(file_path_1, header=None)
            df2 = pd.read_csv(file_path_2, header=None)

            # 验证数据的尺寸是否正确
            if df1.shape[1] < 9 or df2.shape[1] < 9:
                print(f"文件 {file_1} 或 {file_2} 的列数小于9，跳过。")
                continue

            # 创建新的 DataFrame 来保存合并的数据
            merged_df = pd.DataFrame()

            # 添加 EEG1.csv 的前八列
            merged_df = pd.concat([merged_df, df1.iloc[:, :8]], axis=1)

            # 计算 EEG1.csv 的第九列和 time_segment_1.csv 的第一列的平均值
            merged_df[8] = df1.iloc[:, 8] + df2.iloc[:, 0]
            merged_df[8] /= 2

            # 添加 time_segment_1.csv 的第二列到第九列
            merged_df = pd.concat([merged_df, df2.iloc[:, 1:9]], axis=1)

            # 保存合并后的文件
            merged_df.to_csv(os.path.join(output_path, f'merged_{num}.csv'), index=False, header=False)


# 指定目录路径
base_path_1 = 'F:/SEED-VIG数据集/20.数据填充/1'
base_path_2 = 'F:/SEED-VIG数据集/14.数据填充/1'
output_base_path = 'F:/SEED-VIG数据集/21.拼接对称商微分熵/1'

# 调用函数
merge_and_save_csv_files(base_path_1, base_path_2, output_base_path)