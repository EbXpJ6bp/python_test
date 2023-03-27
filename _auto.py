import win32gui
import pyautogui
import pyperclip
import time
from tqdm import tqdm
from datetime import datetime
import os



# このプログラムはウィンドウの設定、パスの更新、ファイル名の更新、Histogramの実行、スクリーンショットのみを自動化します。
# それ以外の設定は前もって手動で設定してください。
# 全部クラスでまとめればいいのにね


def clear_text(x, y):
    pyautogui.click(x, y)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')

def set_text(x, y, string_):
    pyautogui.click(x, y)
    pyperclip.copy(string_)
    pyautogui.hotkey('ctrl', 'v')

def copy_text(x, y):
    pyautogui.click(x, y)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    return pyperclip.paste()

def set_window(x, y, width, heigh):
    time.sleep(1)
    TC_win = win32gui.FindWindow(None, 'Time Controller')
    time.sleep(1)
    if not TC_win:
        print(f'{time.time()}: Not fund "Time Controller.exe"')
        exit()
    win32gui.SetForegroundWindow(TC_win)
    win32gui.MoveWindow(TC_win, x, y, width, heigh, True)
    return TC_win

def update_file_path(window, string_):
    X, Y = 170, 693
    file_path = string_
    win32gui.SetForegroundWindow(window)
    clear_text(X, Y)
    set_text(X, Y, file_path)

def update_file_name(window, string_):
    X, Y = 292, 778
    pre_text = 'Results_Histogram'
    fine_name = f"{pre_text}_{string_}ps_"
    win32gui.SetForegroundWindow(window)
    clear_text(X, Y)
    set_text(X, Y, fine_name)

def get_acquisition_time(window):
    X, Y = 204, 578
    win32gui.SetForegroundWindow(window)
    text = copy_text(X, Y)
    return text

def run_acquisition(window):
    X, Y = 199, 505
    win32gui.SetForegroundWindow(window)
    pyautogui.click(X, Y)

def take_screenshot(window, file_path):
    win32gui.SetForegroundWindow(window)
    window_size = win32gui.GetWindowRect(window)
    prtsc_range = window_size
    pyautogui.screenshot(file_path, region=prtsc_range)

def run_TC(path='AAA', delay=80.0):
    # 進捗表示
    tqdm.write(f'Preparing {delay}[ps]...')

    # Time Controller.exe の表示設定
    hwnd = set_window(-7, 0, 1600, 900)
    time.sleep(1)

    # ファイルパスの設定
    FOLDER_NAME = "origin"
    current_directory = os.path.join(path, FOLDER_NAME)
    update_file_path(hwnd, current_directory)
    time.sleep(1)

    # ファイル名の設定
    file_name = str(delay).replace(".", "_")
    update_file_name(hwnd, file_name)
    time.sleep(1)

    # 実行予定時間の取得
    acquisition_time = int(get_acquisition_time(hwnd))

    # 実行
    tqdm.write(f'Running {delay}[ps]...')
    run_acquisition(hwnd)
    margin_time = 5
    pbar_run = tqdm(range(acquisition_time+margin_time), leave=False, position=0)
    for i in pbar_run:
        pbar_run.set_description(f"Acquisition Progress {i}s")
        time.sleep(1)

    # スクリーンショット
    screenshot_name = f"{datetime.now():%Y-%m-%dT%H_%M_%S}.png"
    screenshot_path = os.path.join(path, screenshot_name)
    take_screenshot(hwnd, screenshot_path)
    tqdm.write(f'Saved {screenshot_name}.')


if __name__ == "__main__":
    run_TC()
