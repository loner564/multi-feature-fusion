import pandas as pd
import numpy as np
import os

# 定义通道对映射关系
channel_mapping = {
    0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6, 8: 9, 9: 8, 10: 11, 11: 10, 12: 13, 13: 12
}

# 大文件夹路径
base_folder = "F:/SEED-VIG数据集/15.提14通道/1"

# 遍历四个子文件夹
subfolders = ["1", "2", "3",]
for subfolder in subfolders:
    # 子文件夹路径
    subfolder_path = os.path.join(base_folder, subfolder)
    # 创建新的子文件夹用于保存结果
    output_folder = os.path.join(base_folder, "F:/SEED-VIG数据集/16.对称商/1", subfolder)
    os.makedirs(output_folder, exist_ok=True)

    # 遍历子文件夹下的所有CSV文件
    for filename in os.listdir(subfolder_path):
        if filename.endswith(".csv"):
            # 读取CSV文件
            file_path = os.path.join(subfolder_path, filename)
            df = pd.read_csv(file_path)

            # 检查DataFrame是否有14行
            #if df.shape[0] != 14:
                #print(f"文件 {filename} 的格式不正确：期望有14行，实际有 {df.shape[0]} 行")
                #continue

            # 计算平均商并生成值
            average_symmetric_diff_values = []
            for channel_1, channel_2 in channel_mapping.items():
                channel_1_data = df.iloc[channel_1 - 1].values
                channel_2_data = df.iloc[channel_2 - 1].values

                # 计算平均对称商
                average_symmetric_diff = np.mean(np.abs(channel_1_data / channel_2_data))
                average_symmetric_diff_values.append(average_symmetric_diff)

            # 创建包含平均对称商的DataFrame
            result_df = pd.DataFrame({
                'Channel': list(channel_mapping.keys()),
                'SQ': average_symmetric_diff_values
            })

            # 保存结果为新的CSV文件，保持原文件名
            result_filename = f"{filename}"
            result_path = os.path.join(output_folder, result_filename)
            result_df.to_csv(result_path, index=False)
            print("平均对称商已保存到新的CSV文件中。")