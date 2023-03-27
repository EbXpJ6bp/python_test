# import serial
import time
from tqdm import tqdm
import subprocess
from subprocess import PIPE
import threading
import sys
import os
from datetime import datetime



def read_stream(in_file, out_file):
    for line in in_file:
        tqdm.write(line.strip(), file=out_file)


def hom_interference_experiment():

    COM = "COM1"
    BIT_RATE = 9600

    # シリアルポートを開く
    try:
       ser = serial.Serial(COM, BIT_RATE)
    except:
       print('Error in serial')
       exit(1)

    # ODLの時間軸を作成
    odl_times = [x / 10 for x in range(800, 1201)]

    # 実行開始時間
    now = datetime.now().strftime('%Y-%m-%dT%H_%M_%S')

    # 実験ディレクトリを作成
    current_dir = os.getcwd()
    dir_name = f'Results_{now}'
    dir_path = os.path.join(current_dir, dir_name)
    os.mkdir(dir_path)

    # ODLの実行
    for odl_time in tqdm(odl_times, desc='Progress in experiment'):
        # 進捗表示
        tqdm.write(f"Time in ODL: {odl_time}[ps]")

        # コマンドを送信
        command = '_ABS_ {0}$\r\n'.format(odl_time)

        print(command)

        exit()

        ser.write(b'{0}'.format(command))

        # OKまたはNGが返ってくるまで待機
        while True:
            response = ser.readline().decode('utf-8').strip()
            if response == 'OK':
                break
            elif response == 'NG':
                print(f'{time.time()}: Error response received: {response}')
                exit()

        # サブプロセスの実行
        p = subprocess.Popen(["python", 'a.py'], stdin=sys.stdin,
                             stdout=PIPE, stderr=PIPE, universal_newlines=True)

        # 並列化によるstdout stderr取得
        th_stdout = threading.Thread(
            target=read_stream, args=(p.stdout, sys.stdout))
        th_stderr = threading.Thread(
            target=read_stream, args=(p.stderr, sys.stderr))
        th_stdout.start()
        th_stderr.start()

        # 実行が終了するまで待つ
        p.wait()
        th_stdout.join()
        th_stdout.join()

        # # 実行結果を表示する
        # tqdm.write(f"{result.stdout}")
        # 進捗表示
        tqdm.write("========================")

    # シリアルポートを閉じる
    # ser.close()


if __name__ == "__main__":
    hom_interference_experiment()
