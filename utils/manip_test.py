import os
import time
import cv2
import numpy as np
import pyautogui
import pygetwindow as gw


def maximize_ai_voice_window(title_keyword="A.I.VOICE2"):
    """
    A.I.VOICE2のウィンドウを最大化して前面に持ってくる
    """
    matching_windows = [
        w for w in gw.getWindowsWithTitle(title_keyword) if w.visible and title_keyword in w.title
    ]
    if not matching_windows:
        raise RuntimeError(f"ウィンドウが見つかりません: {title_keyword}")

    window = matching_windows[0]
    window.activate()
    time.sleep(0.3)
    window.maximize()
    print(f"[✅] Maximized: {window.title}")


def click_button_from_image(image_path: str, threshold=0.8, wait_time=0.3):
    """
    指定された画像を画面上から探してクリックする
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"画像が見つかりません: {image_path}")

    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if template is None:
        raise ValueError(f"画像の読み込みに失敗しました: {image_path}")

    screenshot = pyautogui.screenshot()
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    res = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val < threshold:
        raise ValueError(
            f"{os.path.basename(image_path)}: 一致するボタンが見つかりません (類似度: {max_val:.2f})"
        )

    h, w = template.shape[:2]
    center = (max_loc[0] + w // 2, max_loc[1] + h // 2)
    pyautogui.click(center)
    time.sleep(wait_time)


def prepare_input_area(
    plus_image: str = "resource/plus.png", trash_image: str = "resource/trash.png"
):
    """
    A.I.VOICE2の入力欄を確実にアクティブにする
    """
    maximize_ai_voice_window()
    print("[🖱] Clicking '+' button...")
    click_button_from_image(plus_image)
    print("[🖱] Clicking 'trash' button...")
    click_button_from_image(trash_image)
    print("[✅] 入力欄がアクティブになりました。")


if __name__ == "__main__":
    prepare_input_area()
