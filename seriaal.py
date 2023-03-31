import serial
from tqdm import tqdm
from subprocess import PIPE
import os
from datetime import datetime
import _auto
import time



def serial_tes():

    COM = "COM3"
    BIT_RATE = 9600
    odl_time = 80.0

    # シリアルポートを開く
    ser = serial.Serial(COM, BIT_RATE)


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
                print("OK")
                break
            elif response_m == "NG":
                print(f'{time.time()}: Error response received: {response}')
                ser.close()
                exit()
        except KeyboardInterrupt:
            print('Interrupted')
            ser.close()
            exit()

    # シリアルポートを閉じる
    ser.close()



if __name__ == "__main__":
    serial_tes()
