import os
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling1D, LSTM, Dense, Dropout, Flatten, BatchNormalization
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.manifold import TSNE
import matplotlib.patches as mpatches
from keras.layers import Reshape
from keras.optimizers import Adam
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, roc_auc_score
from keras.callbacks import ModelCheckpoint

# 全局变量
all_data = None
all_labels = None

# 读取数据函数
def load_data(data_folder, categories):
    all_data = []
    all_labels = []

    for all_label, subfolder in enumerate(categories):
        subfolder_path = os.path.join(data_folder, subfolder)
        for file_name in sorted(os.listdir(subfolder_path)):
            file_path = os.path.join(subfolder_path, file_name)
            df = pd.read_csv(file_path, header=None)
            all_data.append(df.values)
            all_labels.append(all_label)

    all_data = np.array(all_data)
    all_labels = np.array(all_labels)

    return all_data, all_labels

# 模型构建函数
def build_improved_model(input_shape):
    model = Sequential()
    model.add(Reshape((23, 17, 1), input_shape=(23, 17)))
    model.add(Conv2D(16, 3, activation='relu', input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(Conv2D(16, 3, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)))
    model.add(BatchNormalization())
    model.add(Conv2D(32, 5, activation='relu'))
    model.add(BatchNormalization())
    model.add(Conv2D(32, 5, activation='relu'))
    model.add(BatchNormalization())

    # 将卷积层的输出转换为三维张量
    model.add(Reshape((-1, 32)))

    model.add(LSTM(32))

    model.add(Dense(16, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(3, activation='softmax'))

    # 定义自定义学习率
    custom_learning_rate = 0.0001
    optimizer = Adam(learning_rate=custom_learning_rate)
    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    return model

# 主函数
def main():
    # 数据读取、模型构建等代码
    data_dir = 'F:/SEED-VIG数据集/23.划分训练测试/1/训练集1'
    categories = ['1', '2', '3']
    input_shape = (23, 17, 1)

    all_data, all_labels = load_data(data_dir, categories)
    train_data, test_data, train_labels, test_labels = train_test_split(
        all_data, all_labels, test_size=0.2, random_state=20)
    model = build_improved_model(input_shape)
    filepath = "F:/SEED-VIG数据集/24.结果/model/the_best_model-{epoch:02d}-{val_accuracy:.2f}.h5"
    # 中途训练效果提升, 则将文件保存, 每提升一次, 保存一次
    checkpoint = ModelCheckpoint(filepath, monitor='val_accuracy', verbose=1, save_best_only=False, mode='auto')
    callbacks_list = [checkpoint]
    history = model.fit(train_data, train_labels,
                        validation_data=(test_data, test_labels),
                        epochs=100, verbose=1, callbacks=callbacks_list)

    #model.save('cnn_lstm_model.h5')

    #tf.keras.utils.plot_model(model, 'model.png', show_shapes=True)

    # 保存训练过程数据
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    epochs = range(len(loss))

    # 保存损失和准确率数据
    pd.DataFrame({'epochs': epochs, 'loss': loss, 'val_loss': val_loss}).to_excel('loss_data.xlsx', index=False)
    pd.DataFrame({'epochs': epochs, 'acc': acc, 'val_acc': val_acc}).to_excel('acc_data.xlsx', index=False)

    # 绘制损失曲线
    plt.plot(epochs, loss, 'bo', label='Training Loss')
    plt.plot(epochs, val_loss, 'ro', label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.legend()
    plt.savefig('loss.png')
    plt.clf()

    # 绘制准确率曲线
    plt.plot(epochs, acc, 'r', label='Training Accuracy')
    plt.plot(epochs, val_acc, 'b', label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.legend()
    plt.savefig('acc.png')
    plt.clf()

    # 模型预测
    y_pred = model.predict(test_data)
    y_pred_classes = np.argmax(y_pred, axis=1)

    # 混淆矩阵和分类报告
    cm = confusion_matrix(test_labels, y_pred_classes)
    print("Confusion Matrix:\n", cm)
    cr = classification_report(test_labels, y_pred_classes, digits=4)
    print("Classification Report:\n", cr)

    # ROC曲线和AUC
    y_true_binary = label_binarize(test_labels, classes=[0, 1])  # 标签二值化
    fpr, tpr, _ = roc_curve(y_true_binary[:, 0], y_pred[:, 0])
    roc_auc = roc_auc_score(y_true_binary[:, 0], y_pred[:, 0])

    plt.figure()
    plt.plot(fpr, tpr, label='ROC curve (area = {0:0.2f})'.format(roc_auc))
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.savefig('ROC.png')
    plt.clf()

    # 保存ROC曲线数据
    pd.DataFrame({'FPR': fpr, 'TPR': tpr, 'AUC': [roc_auc] * len(fpr)}).to_excel('roc_data.xlsx', index=False)


if __name__ == '__main__':
    main()