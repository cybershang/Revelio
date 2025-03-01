import kaggle
import os
from pathlib import Path
import shutil
import re


def download_dataset(dataset_identifier):
    script_dir = os.getcwd()
    try:
        # 初始化 Kaggle API
        kaggle.api.authenticate()
        # 下载数据集到指定目录
        kaggle.api.dataset_download_files(dataset_identifier, path=script_dir, unzip=True)
        print("数据集下载成功！")
    except Exception as e:
        print(f"下载数据集时出现错误: {e}")


def process_files(source_dir, dataset_dir, start_index):
    if source_dir.exists():
        file_index = start_index
        for file in sorted(source_dir.iterdir()):
            if file.is_file():
                new_file_name = f'{file_index}{file.suffix}'
                new_file_path = source_dir / new_file_name
                os.rename(file, new_file_path)
                print(f"重命名 {file} 为 {new_file_path}")
                # 移动文件到 dataset 文件夹
                destination_file = dataset_dir / new_file_name
                shutil.move(new_file_path, destination_file)
                print(f"移动 {new_file_path} 到 {destination_file}")
                file_index += 1


def move_and_delete(source_dir, dataset_dir, num_files=1000):
    if source_dir.exists():
        data_files = os.listdir(source_dir)
        if len(data_files) < num_files:
            print(f"{source_dir} 中文件数量不足 {num_files} 个，只有 {len(data_files)} 个文件。")
        else:
            for file_name in data_files[:num_files]:
                source_file = source_dir / file_name
                destination_file = dataset_dir / file_name
                shutil.move(source_file, destination_file)
            print(f"成功移动 {num_files} 个文件到 {dataset_dir} 文件夹。")
            shutil.rmtree(source_dir)
            print(f"{source_dir} 文件夹已删除。")


# 下载第一个数据集
dataset_identifier_1 = 'mohamedmustafa/real-life-violence-situations-dataset'
download_dataset(dataset_identifier_1)

# 获取当前工作目录
current_dir = Path.cwd()

# 定义 Real Life Violence Dataset 文件夹的路径
violence_dataset_dir = current_dir / 'Real Life Violence Dataset'

# 定义 dataset 文件夹的路径
dataset_dir = current_dir / 'dataset'

# 创建 dataset 文件夹（如果不存在）
if not dataset_dir.exists():
    dataset_dir.mkdir()

# 检查 Real Life Violence Dataset 文件夹是否存在
if not violence_dataset_dir.exists():
    print(f"文件夹 {violence_dataset_dir} 不存在。")
else:
    # 处理 NonViolence 文件夹
    non_violence_dir = violence_dataset_dir / 'NonViolence'
    process_files(non_violence_dir, dataset_dir, 1)

    # 处理 Violence 文件夹
    violence_dir = violence_dataset_dir / 'Violence'
    process_files(violence_dir, dataset_dir, 1001)

    # 递归删除 Real Life Violence Dataset 文件夹
    if violence_dataset_dir.exists():
        shutil.rmtree(violence_dataset_dir)
        print(f"删除文件夹 {violence_dataset_dir}")

    # 递归删除 real life violence situations 文件夹
    real_life_situations_dir = current_dir / 'real life violence situations'
    if real_life_situations_dir.exists():
        shutil.rmtree(real_life_situations_dir)
        print(f"删除文件夹 {real_life_situations_dir}")

# 下载第二个数据集
dataset_identifier_2 = 'yassershrief/hockey-fight-vidoes'
download_dataset(dataset_identifier_2)

# 定义 data_hockey 文件夹的路径
data_hockey_dir = current_dir / 'data'

# 检查 data_hockey 文件夹是否存在
if not data_hockey_dir.exists():
    print(f"文件夹 {data_hockey_dir} 不存在。")
else:
    # 重命名文件
    file_list = sorted(data_hockey_dir.iterdir())
    new_number = 2001
    for file in file_list:
        if file.is_file():
            new_file_name = data_hockey_dir / f'{new_number}{file.suffix}'
            os.rename(file, new_file_name)
            print(f"重命名 {file} 为 {new_file_name}")
            new_number += 1

    move_and_delete(data_hockey_dir, dataset_dir, 1000)
    