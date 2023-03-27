import _convert
import _extract
import os
from tqdm import tqdm



if __name__ == "__main__":

    # フォルダー内の全てのフォルダーを取得
    current_dir = os.getcwd()
    folders = os.listdir(current_dir)

    # フォルダーを日付順にソート
    folders.sort()


    for folder in folders:
        if folder.startswith("Results_"):
            # フォルダー名から日付を取得
            folder_path = os.path.join(current_dir, folder)

            origin_folder_path = os.path.join(folder_path, "origin")
            comma_folder_path = os.path.join(folder_path, "comma")

            _convert.semicolon_to_comma(origin_folder_path, comma_folder_path)

            _extract.hom_interference_experiment_result(folder_path, comma_folder_path)

            new_path = os.path.join(current_dir, f"Done_{folder}")
            os.rename(folder_path, new_path)

