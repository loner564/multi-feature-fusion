from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import os
from sklearn.metrics import classification_report, confusion_matrix

# 加载保存的模型
model_path = "F:/SEED-VIG数据集/24.结果/model/the_best_model-100-0.87.h5"  # 替换为您保存的模型路径
model = load_model(model_path)

# 定义加载数据的函数
def load_data(data_folder, categories):
    all_data = []
    all_labels = []
    for all_label, subfolder in enumerate(categories):  # 遍历每个类别
        subfolder_path = os.path.join(data_folder, subfolder)
        for file_name in sorted(os.listdir(subfolder_path)):  # 遍历每个文件
            file_path = os.path.join(subfolder_path, file_name)
            df = pd.read_csv(file_path, header=None)  # 读取CSV文件
            all_data.append(df.values)  # 添加数据
            all_labels.append(all_label)  # 添加对应标签
    all_data = np.array(all_data)
    all_labels = np.array(all_labels)
    return all_data, all_labels

# 验证集路径和分类类别
validation_path = "F:/SEED-VIG数据集/23.划分训练测试/1/测试集1"  # 替换为您的验证集路径
categories = ['1', '2', '3']  # 定义类别

# 加载验证集数据
val_features, val_labels = load_data(validation_path, categories)

# 检查加载数据的形状
print(f"验证集特征形状: {val_features.shape}")
print(f"验证集标签形状: {val_labels.shape}")

# 确保模型输入和数据形状一致
# 模型预测
val_features = val_features.reshape(val_features.shape[0], -1, val_features.shape[-1])  # 调整输入维度
y_pred = model.predict(val_features)

# 获取预测类别
y_pred_classes = np.argmax(y_pred, axis=1)

# 计算准确率
accuracy = np.mean(y_pred_classes == val_labels)
print(f'Accuracy: {accuracy:.4f}')

# 计算混淆矩阵和分类报告
cm = confusion_matrix(val_labels, y_pred_classes)
print('Confusion Matrix:')
print(cm)

cr = classification_report(val_labels, y_pred_classes, target_names=categories)
print('Classification Report:')
print(cr)

# 遍历验证集以显示预测结果和真实标签
for i, (pred, label) in enumerate(zip(y_pred_classes, val_labels)):
    print(f'Sample {i}: Predicted label = {pred}, True label = {label}')