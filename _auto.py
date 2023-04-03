import win32gui
import pyautogui
import pyperclip
import time
from tqdm import tqdm
from datetime import datetime
import os
from PIL import Image


class TimeController:
    def __init__(self, path='AAA', delay=80.0):
        self.path = path
        self.delay = delay
        self.window_title = 'Time Controller'
        self.folder_name = 'raw'
        self.file_path_xy = (170, 693)
        self.file_name_xy = (292, 778)
        self.acquisition_time_xy = (204, 578)
        self.run_acquisition_xy = (199, 505)
        self.window = None
        self.acquisition_time = 0
        self.margin_time = 5
        self.get_window()

    def clear_text(self, x, y):
        pyautogui.click(x, y)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')

    def set_text(self, x, y, string_):
        pyautogui.click(x, y)
        pyperclip.copy(string_)
        pyautogui.hotkey('ctrl', 'v')

    def copy_text(self, x, y):
        pyautogui.click(x, y)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        return pyperclip.paste()

    def get_window(self):
        time.sleep(1)
        self.window = win32gui.FindWindow(None, self.window_title)
        time.sleep(1)
        if not self.window:
            print(f'{time.time()}: Not found "{self.window_title}.exe"')
            exit()

    def set_window(self):
        # workground: https://stackoverflow.com/questions/51694887/win32gui-movewindow-not-aligned-with-left-edge-of-screen
        x, y, width, height = -7, 0, 1600, 900
        win32gui.SetForegroundWindow(self.window)  # type: ignore
        win32gui.MoveWindow(self.window, x, y, width, height, True)  # type: ignore

    def update_file_path(self):
        current_directory = os.path.join(self.path, self.folder_name)
        self.set_window()
        self.clear_text(*self.file_path_xy)
        self.set_text(*self.file_path_xy, current_directory)

    def update_file_name(self):
        pre_text = 'Results_Histogram'
        delay_text = str(self.delay).replace(".", "_")
        file_name = f"{pre_text}_{delay_text}ps_"
        self.set_window()
        self.clear_text(*self.file_name_xy)
        self.set_text(*self.file_name_xy, file_name)

    def get_acquisition_time(self):
        self.set_window()
        text = self.copy_text(*self.acquisition_time_xy)
        return int(text)

    def prepare_acquisition(self):
        self.set_window()
        self.update_file_path()
        self.update_file_name()
        self.acquisition_time = self.get_acquisition_time()

    def run_acquisition(self):
        self.set_window()
        pyautogui.click(*self.run_acquisition_xy)

    def take_screenshot(self):
        pre_text = 'Results_Histogram_'
        delay_text = str(self.delay).replace(".", "_")
        saved_time_text = datetime.now().strftime('%Y-%m-%dT%H_%M_%S')
        screenshot_name = f"{pre_text}_{delay_text}_{saved_time_text}.png"
        screenshot_path = os.path.join(self.path, screenshot_name)
        window_size = win32gui.GetWindowRect(self.window)  # type: ignore
        prtsc_range = window_size
        pyautogui.screenshot(screenshot_path, region=prtsc_range)

    def run_TC(self):
        # 準備
        tqdm.write(f'TIA: Preparing...')
        self.prepare_acquisition()

        # 実行
        tqdm.write(f'TIA: Running...')
        self.run_acquisition()
        pbar_run = tqdm(range(self.acquisition_time + self.margin_time), leave=False, position=0)
        for i in pbar_run:
            pbar_run.set_description(f"Acquisition Progress {i}s")
            time.sleep(1)

        self.take_screenshot()


def main(path, delay):
    myclass = TimeController(path, delay)
    myclass.run_TC()


if __name__ == "__main__":
    main(path='AAA', delay=80.0)

