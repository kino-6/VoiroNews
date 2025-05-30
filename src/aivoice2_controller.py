import os
import time
import ctypes
import win32gui
import win32con
import pyperclip
import pyautogui
import cv2
import numpy as np
import pygetwindow as gw
from tts_controller import TTSStrategy
import time


class AIVoice2Controller(TTSStrategy):
    def __init__(
        self,
        window_title_keyword="A.I.VOICE2 Editor",
        image_dir="../resource",
        plus_image="plus.png",
        trash_image="trash.png",
        play_image="play_all.png",
    ):
        self.window_title_keyword = window_title_keyword
        self.image_dir = image_dir
        self.plus_image_path = os.path.join(image_dir, plus_image)
        self.trash_image_path = os.path.join(image_dir, trash_image)
        self.play_image_path = os.path.join(image_dir, play_image)

    def maximize_ai_voice_window(self):
        """
        A.I.VOICE2のウィンドウを最大化して前面に持ってくる
        """
        matching_windows = [
            w
            for w in gw.getWindowsWithTitle(self.window_title_keyword)
            if w.visible and self.window_title_keyword in w.title
        ]

        if not matching_windows:
            raise RuntimeError(f"ウィンドウが見つかりません: {self.window_title_keyword}")

        window = matching_windows[0]
        window.activate()
        time.sleep(0.3)
        window.maximize()
        print(f"[✅] Maximized: {window.title}")
        return window._hWnd  # 後でフォーカスを戻すときに使える

    def click_image(self, image_path, y_offset=0, confidence=0.8):
        screenshot = pyautogui.screenshot()
        screen_np = np.array(screenshot)
        screen_rgb = cv2.cvtColor(screen_np, cv2.COLOR_BGR2RGB)
        template = cv2.imread(image_path)

        if template is None:
            raise FileNotFoundError(f"Template image not found: {image_path}")

        result = cv2.matchTemplate(screen_rgb, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val < confidence:
            raise RuntimeError(f"Image not found on screen: {image_path} (confidence={max_val})")

        h, w = template.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2 + y_offset
        pyautogui.click(center_x, center_y)
        time.sleep(0.3)

    def prepare_input_area(self):
        self.maximize_ai_voice_window()
        self.click_image(self.plus_image_path)
        self.click_image(self.trash_image_path)
        # 🧹 入力欄をクリア（Ctrl + A → Del）
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('delete')
        time.sleep(0.2)
        print("[✅] 入力欄クリア完了")

    def speak(self, text: str):
        original_hwnd = win32gui.GetForegroundWindow()

        # クリップボードにコピー
        pyperclip.copy(text)
        time.sleep(0.1)

        # 入力欄の準備（+ → ゴミ箱）
        self.prepare_input_area()

        # Ctrl+V で貼り付け
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.2)

        # 再生ボタンを押す
        self.click_image(self.play_image_path)

        # 元のウィンドウに戻す
        if original_hwnd and win32gui.IsWindow(original_hwnd):
            win32gui.ShowWindow(original_hwnd, win32con.SW_SHOW)
            win32gui.SetForegroundWindow(original_hwnd)
