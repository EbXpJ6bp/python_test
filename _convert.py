import os
from tqdm import tqdm
import time
import sys


def semicolon_to_comma():
    NEW_SUFFIX = "_C"

    current_dir = os.getcwd()
    folder_path = os.path.join(current_dir, "original")
    folder_path_to_save = os.path.join(current_dir, "comma")

    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    for file_name in tqdm(files , desc='Progress in convert'):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "r") as f:
            content = f.read()
        content = content.replace(";", ",")
        new_file_name = os.path.splitext(os.path.basename(file_path))[0] + NEW_SUFFIX + ".csv"
        new_file_path = os.path.join(folder_path_to_save, new_file_name)
        with open(new_file_path, "w") as f:
            f.write(content)


if __name__ == "__main__":
    semicolon_to_comma()
