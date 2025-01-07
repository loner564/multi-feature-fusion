import os
import shutil
from sklearn.model_selection import KFold

# 原始路径和目标路径
base_path = r"F:\SEED-VIG数据集\22.三特征融合\1"
test_train_folder = r"F:\SEED-VIG数据集\23.划分训练测试\1"

# 遍历子文件夹
subfolders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]

# 创建测试集和训练集文件夹
for i in range(1, 11):
    os.makedirs(os.path.join(test_train_folder, f"测试集{i}"), exist_ok=True)
    os.makedirs(os.path.join(test_train_folder, f"训练集{i}"), exist_ok=True)

# 分别处理每个子文件夹
for subfolder in subfolders:
    subfolder_path = os.path.join(base_path, subfolder)
    csv_files = [f for f in os.listdir(subfolder_path) if f.endswith('.csv')]

    # 创建 10 份数据
    kf = KFold(n_splits=10, shuffle=True, random_state=42)
    splits = list(kf.split(csv_files))

    # 为每个分组处理测试集和训练集
    for i, (train_idx, test_idx) in enumerate(splits):
        test_folder = os.path.join(test_train_folder, f"测试集{i + 1}", subfolder)
        train_folder = os.path.join(test_train_folder, f"训练集{i + 1}", subfolder)

        # 创建子文件夹
        os.makedirs(test_folder, exist_ok=True)
        os.makedirs(train_folder, exist_ok=True)

        # 将测试文件拷贝到测试集文件夹
        for idx in test_idx:
            test_file = csv_files[idx]
            shutil.copy(os.path.join(subfolder_path, test_file), os.path.join(test_folder, test_file))

        # 将训练文件拷贝到训练集文件夹
        for idx in train_idx:
            train_file = csv_files[idx]
            shutil.copy(os.path.join(subfolder_path, train_file), os.path.join(train_folder, train_file))

print("数据集分割完成！")