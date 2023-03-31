import serial
from tqdm import tqdm
from subprocess import PIPE
import os
from datetime import datetime
import _auto
import time


def read_stream(in_file, out_file):
    for line in in_file:
        tqdm.write(line.strip(), file=out_file)


def hom_interference_experiment():

    COM = "COM3"
    BIT_RATE = 9600

    # シリアルポートを開く
    ser = serial.Serial(COM, BIT_RATE)

    # ODLの時間軸を作成
    odl_times = [x / 10 for x in range(800, 810)]

    # 実行開始時間
    experiment_start_time = datetime.now().strftime('%Y-%m-%dT%H_%M_%S')

    # 実験ディレクトリを作成
    current_dir = os.getcwd()
    dir_name = f'Results_{experiment_start_time}'
    dir_path = os.path.join(current_dir, dir_name)
    os.mkdir(dir_path)

    # ODLの実行
    pbar = tqdm(odl_times, position=1, leave=True)
    for odl_time in pbar:
        # 進捗表示
        pbar.set_description(f'Progress in Experiment (delay {odl_time}[ps])')

        # コマンドを送信
        command = '_ABS_ {0}$\r\n'.format(odl_time)
        command_b = command.encode('utf-8')
        ser.write(command_b)

        # OKまたはNGが返ってくるまで待機
        # TODO: read()が1文字ずつ返してくるのに対して、無理やりな実装なので注意
        response_m = ''
        while True:
            try:
                response = ser.read().strip().decode('UTF-8')
                response_m += response
                if response_m == 'OK':
                    tqdm.write(f"ODL: Set to {odl_time}[ps]")
                    break
                elif response_m == "NG":
                    tqdm.write(
                        f'{time.time()}: Error response received: {response}, TDL tried to set {odl_time}[ps]')
                    ser.close()
                    exit()
            except KeyboardInterrupt:
                print('Interrupted')
                ser.close()
                exit()

        # Time Controllerの制御
        _auto.run_TC(dir_path, odl_time)

    # シリアルポートを閉じる
    ser.close()

    experiment_end_time = datetime.now().strftime('%Y-%m-%dT%H_%M_%S')

    time.sleep(1)
    print("=========")
    print("おわったあ！！")
    print(f"終了時刻: {experiment_end_time}")


if __name__ == "__main__":
    hom_interference_experiment()
