import os
import time
import win32gui
import win32con
from pywinauto import Application
from tts_controller import TTSStrategy


class VoiceroidController(TTSStrategy):
    def __init__(self, exe_path=None):
        self.exe_path = exe_path or self._find_exe_path()
        self.app = None
        self.window = None

    def _find_exe_path(self):
        possible_paths = [
            os.path.expandvars(r"%ProgramFiles(x86)%\AHS\VOICEROID2\VoiceroidEditor.exe"),
            os.path.expandvars(r"%ProgramFiles%\AHS\VOICEROID2\VoiceroidEditor.exe"),
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        raise FileNotFoundError("VoiceroidEditor.exe が見つかりません。")

    def exists(self):
        try:
            self.app = Application(backend="uia").connect(path=self.exe_path)
            self.window = self.app.window(title_re=".*VOICEROID2.*")
            return True
        except Exception:
            return False

    def launch(self):
        self.app = Application(backend="uia").start(self.exe_path)
        self.window = self.app.window(title_re=".*VOICEROID2.*")
        self.window.wait("visible", timeout=15)

    def refresh_or_launch(self):
        if not self.exists():
            self.launch()

    def find_button_by_label_text(self, label_text="音声保存", raise_error=True):
        buttons = self.window.descendants(control_type="Button")
        for btn in buttons:
            try:
                texts = btn.descendants(control_type="Text")
                for t in texts:
                    if t.window_text() == label_text:
                        return btn
            except Exception:
                continue
        if raise_error:
            raise RuntimeError(f"ボタンラベル '{label_text}' が見つかりません")
        return None

    def wait_until_ready(self, timeout=10):
        for _ in range(timeout * 10):
            try:
                save_button = self.find_button_by_label_text("音声保存", raise_error=False)
                if save_button and save_button.is_enabled():
                    return True
            except Exception:
                pass
            time.sleep(0.1)
        raise TimeoutError("音声保存ボタンが有効化されませんでした")

    def wait_until_finished(self, timeout=60):
        for _ in range(timeout * 10):
            try:
                texts = self.window.descendants(control_type="Text")
                for t in texts:
                    if "完了" in t.window_text():
                        return
            except Exception:
                pass
            time.sleep(0.1)
        raise TimeoutError("読み上げが完了しませんでした")

    def speak(self, text):
        original_hwnd = win32gui.GetForegroundWindow()
        self.refresh_or_launch()
        self.wait_until_ready()

        text_box = self.window.child_window(auto_id="TextBox", control_type="Edit")
        text_box.set_edit_text(text)

        play_button = self.find_button_by_label_text("再生")
        play_button.click_input()

        if original_hwnd and win32gui.IsWindow(original_hwnd):
            win32gui.ShowWindow(original_hwnd, win32con.SW_SHOW)
            win32gui.SetForegroundWindow(original_hwnd)

        self.wait_until_finished()

    def close(self):
        if self.window:
            self.window.close()
