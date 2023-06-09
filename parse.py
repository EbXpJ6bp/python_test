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

    # 未処理のフォルダーを検索
    folders = [f for f in os.listdir(current_dir) if f.startswith("Results_")]

    if not folders:
        print("未処理のフォルダーがありません")
        exit()

    for folder in tqdm(folders, desc='Progress in parse', position=1):
        # 処理に使うパスを管理
        folder_path = os.path.join(current_dir, folder)
        raw_folder_path = os.path.join(folder_path, "raw")
        comma_folder_path = os.path.join(folder_path, "comma")

        # 変換と、抽出を実行
        _convert.semicolon_to_comma(raw_folder_path, comma_folder_path)
        _extract.hom_interference_experiment_result(folder_path, comma_folder_path)

        # 処理が終わったファイルの名前を変更
        new_folder_path = os.path.join(current_dir, f"Done_{folder}")
        os.rename(folder_path, new_folder_path)
