# import serial
import time
from tqdm import tqdm
import subprocess
from subprocess import PIPE
import threading
import sys
import os
from datetime import datetime
import _auto



def read_stream(in_file, out_file):
    for line in in_file:
        tqdm.write(line.strip(), file=out_file)


def hom_interference_experiment():

    COM = "COM1"
    BIT_RATE = 9600

    # シリアルポートを開く
    # try:
    #    ser = serial.Serial(COM, BIT_RATE)
    # except:
    #    print('Error in serial')
    #    exit(1)

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
    pbar = tqdm(odl_times, desc='Progress in experiment', position=1)
    for odl_time in pbar:
        # 進捗表示
        pbar.set_description(f'Progress in experiment (delay {odl_time})')

        # コマンドを送信
        command = '_ABS_ {0}$\r\n'.format(odl_time)

        # print(command)

        # ser.write(b'{0}'.format(command))

        # # OKまたはNGが返ってくるまで待機
        # while True:
        #     response = ser.readline().decode('utf-8').strip()
        #     if response == 'OK':
        #         break
        #     elif response == 'NG':
        #         print(f'{time.time()}: Error response received: {response}')
        #         exit()

        # Time Controllerの制御
        _auto.run_TC(dir_path, odl_time)



    # シリアルポートを閉じる
    # ser.close()


if __name__ == "__main__":
    hom_interference_experiment()
