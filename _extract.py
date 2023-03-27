import os
import pandas as pd
import re
import time
from datetime import datetime
from tqdm import tqdm


def hom_interference_experiment_result(working_dir, comma_folder_path):

    # .csvファイルのリストを取得
    csv_files = [f for f in os.listdir(comma_folder_path) if f.endswith('.csv')]

    # .csvファイルの内容を格納する辞書を初期化
    csv_dict = {}

    # 縦軸と横軸のフィルター
    row_filter = [4750, 4850, 4950, 5050, 5150, 5250, 5350, 5450, 5550,
                  5650, 5750, 5850, 5950, 6050, 6150, 6250, 6350, 6450, 6550, 6650]
    col_filter = 'Histo02'

    # my_list = list(range(4750, 6651, 100))
    # print(my_list)

    # .csvファイルを1つずつ処理
    for csv_file in tqdm(csv_files, desc='Progress in extract', leave=False, position=0):

        # .csvファイルを読み込み、indexをTIA_timeになるように調整
        df = pd.read_csv(os.path.join(comma_folder_path, csv_file), index_col=0)

        # 縦軸と横軸のフィルターを適用
        # TODO: 以上、以下で指定してもいい
        ser = df.loc[row_filter, col_filter]

        # 列名を遅延量に変更
        new_col_name = re.search(r"\d+(_\d+)?", csv_file[:-4]).group(0).replace("_", ".")
        if new_col_name is None:
            print(f'{time.time()}: Error in Regular expression')
            exit()
        ser.name = new_col_name

        # 辞書に追加
        csv_dict[new_col_name] = ser

    # 辞書をODLの小さい順からソート
    csv_dict_s = dict(sorted(csv_dict.items(), key=lambda x: float(x[0])))

    # 辞書を結合
    result_df = pd.concat(csv_dict_s.values(), axis=1)

    # 結果を保存
    result_df.to_csv(os.path.join(working_dir, f"extracted_{datetime.now():%Y-%m-%dT%H_%M_%S}.csv"))


if __name__ == "__main__":

    # フォルダーのパス
    working_dir = os.getcwd()
    comma_folder_path = os.path.join(working_dir, "comma")
    hom_interference_experiment_result(working_dir, comma_folder_path)
