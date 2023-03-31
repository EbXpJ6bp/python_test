import os
from tqdm import tqdm
import time
import sys


def semicolon_to_comma(folder_path_to_ref, folder_path_to_save):
    NEW_SUFFIX = "_C"

    files = [f for f in os.listdir(folder_path_to_ref) if f.endswith('.csv')]

    for file_name in tqdm(files , desc='Progress in convert', leave=False, position=0):
        # ファイルの読み取り
        file_path = os.path.join(folder_path_to_ref, file_name)
        with open(file_path, "r") as f:
            content = f.read()

        # 置換
        content = content.replace(";", ",")

        # 新しいファイルを作成(上書き)
        new_file_name = os.path.splitext(os.path.basename(file_path))[0] + NEW_SUFFIX + ".csv"
        os.makedirs(folder_path_to_save, exist_ok=True)
        new_file_path = os.path.join(folder_path_to_save, new_file_name)
        with open(new_file_path, "w") as f:
            f.write(content)

if __name__ == "__main__":
    current_dir = os.getcwd()
    raw_folder_path = os.path.join(current_dir, "raw")
    comma_folder_path = os.path.join(current_dir, "comma")

    semicolon_to_comma(raw_folder_path, comma_folder_path)
