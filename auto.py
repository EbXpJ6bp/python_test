import win32gui
import pyautogui
import pyperclip
import time


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


def run_acquisition(window):
    X, Y = 199, 505
    win32gui.SetForegroundWindow(window)
    pyautogui.click(X, Y)


def take_screenshot(window, file_path):
    win32gui.SetForegroundWindow(window)
    window_size = win32gui.GetWindowRect(window)
    prtsc_range = window_size
    pyautogui.screenshot(file_path, region=prtsc_range)


def main():
    # 引数 実行時間、実験名、遅延寮の予定

    # Time Controller.exe の表示設定
    hwnd = set_window(-7, 0, 1600, 900)
    time.sleep(1)

    # ファイルパスの設定
    update_file_path(hwnd, 'AAA')
    time.sleep(1)

    # ファイル名の設定
    update_file_name(hwnd, 'AAA')
    time.sleep(1)

    # 実行
    run_acquisition(hwnd)
    time.sleep(1)

    # スクリーンショット
    take_screenshot(hwnd, 'test.png')


if __name__ == "__main__":
    main()
