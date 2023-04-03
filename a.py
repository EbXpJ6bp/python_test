import win32gui
import pyautogui
import pyperclip
import time
from tqdm import tqdm
from datetime import datetime
import os
from PIL import Image


# このプログラムはウィンドウの設定、パスの更新、ファイル名の更新、Histogramの実行、スクリーンショットのみを力技で自動化します。
# それ以外の設定は前もって手動で設定してください。
# クラスでまとめればいいのにね


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


def get_window():
    time.sleep(1)
    TC_win = win32gui.FindWindow(None, 'Time Controller')
    time.sleep(1)
    if not TC_win:
        print(f'{time.time()}: Not fund "Time Controller.exe"')
        exit()
    return TC_win


def set_window(window):
    # workground: https://stackoverflow.com/questions/51694887/win32gui-movewindow-not-aligned-with-left-edge-of-screen
    X, Y, WIDTH, HEIGH = -7, 0, 1600, 900
    win32gui.SetForegroundWindow(window)
    win32gui.MoveWindow(window, X, Y, WIDTH, HEIGH, True)


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

    # screenshot = pyautogui.screenshot(region=prtsc_range)
    # image = Image.frombytes('RGB', screenshot.size, screenshot.tobytes())
    # image.save(file_path, 'JPEG', quality=70)


def run_TC(path='AAA', delay=80.0):
    # 進捗表示
    tqdm.write(f'TIA: Preparing...')

    # Time Controller.exe の表示設定
    hwnd = get_window()
    set_window(hwnd)

    # ファイルパスの設定
    FOLDER_NAME = "raw"
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
    tqdm.write(f'TIA: Running...')
    run_acquisition(hwnd)
    margin_time = 5
    pbar_run = tqdm(range(acquisition_time+margin_time),
                    leave=False, position=0)
    for i in pbar_run:
        pbar_run.set_description(f"Acquisition Progress {i}s")
        time.sleep(1)

    # スクリーンショットを取得
    # こっち側の内容が重すぎ
    pre_text = 'Results_Histogram_png'
    delay_text = str(delay).replace(".", "_")
    saved_time_text = datetime.now().strftime('%Y-%m-%dT%H_%M_%S')
    screenshot_name = f"{pre_text}_{delay_text}ps_{saved_time_text}.png"
    screenshot_path = os.path.join(path, screenshot_name)
    take_screenshot(hwnd, screenshot_path)


if __name__ == "__main__":
    run_TC()
