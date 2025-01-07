import scipy.io
import shutil
import os

# 读取MAT文件
mat_file_path = "F:/SEED-VIG/三分类/perclos1.mat"
mat = scipy.io.loadmat(mat_file_path)
data = mat['data'].flatten()

# 源文件夹和目标文件夹路径
source_folder = "F:/SEED-VIG数据集/11.映射/1/14-31/"
target_folder_base = "F:/SEED-VIG数据集/12.分类/1/"

# 遍历并移动文件
for i in range(885):
  source_file = source_folder + f"time_segment_{i+1}.csv"
  target_folder = target_folder_base + str(data[i])
  if not os.path.exists(target_folder):
    os.makedirs(target_folder)
  shutil.move(source_file, target_folder)