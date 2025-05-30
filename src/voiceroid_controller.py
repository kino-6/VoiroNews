import os
import time
import win32gui
import win32con
from pywinauto import Application


class VoiceroidController:
    def __init__(self, exe_path=None):
        self.exe_path = exe_path or self._find_exe_path()
        self.app = None
        self.window = None

    def _find_exe_path(self):
        """VoiceroidEditor.exe を探す"""
        possible_paths = [
            os.path.expandvars(r"%ProgramFiles(x86)%\AHS\VOICEROID2\VoiceroidEditor.exe"),
            os.path.expandvars(r"%ProgramFiles%\AHS\VOICEROID2\VoiceroidEditor.exe"),
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        raise FileNotFoundError(
            "VoiceroidEditor.exe が見つかりません。インストールされていますか？"
        )

    def exists(self):
        """既に起動しているか"""
        try:
            self.app = Application(backend="uia").connect(path=self.exe_path)
            self.window = self.app.window(title_re=".*VOICEROID2.*")
            return True
        except Exception:
            return False

    def launch(self):
        """Voiceroid2 を起動"""
        self.app = Application(backend="uia").start(self.exe_path)
        self.window = self.app.window(title_re=".*VOICEROID2.*")
        self.window.wait("visible", timeout=15)

    def refresh_or_launch(self):
        """既存接続 or 起動"""
        if not self.exists():
            self.launch()

    def find_button_by_label_text(self, label_text="音声保存", raise_error=True):
        """ボタン内に指定ラベル（Static）を含むボタンを探す"""
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
            raise RuntimeError(f"ボタンラベル '{label_text}' を持つボタンが見つかりませんでした")
        return None

    def wait_until_ready(self, timeout=10):
        """音声保存ボタンが有効になるまで待機"""
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
        """ステータステキストに '完了' を含むかどうかで判定"""
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
        """指定テキストを入力して読み上げ（非同期で元のウィンドウに戻す）"""
        # フォーカス中のウィンドウを取得
        original_hwnd = win32gui.GetForegroundWindow()

        # 起動 or 再接続
        self.refresh_or_launch()
        self.wait_until_ready()

        # テキスト入力欄にセット
        text_box = self.window.child_window(auto_id="TextBox", control_type="Edit")
        text_box.set_edit_text(text)

        # 再生ボタンをクリック
        play_button = self.find_button_by_label_text("再生")
        play_button.click_input()

        # ✅ ここでフォーカスを元に戻す（読み上げはバックグラウンドで継続）
        if original_hwnd and win32gui.IsWindow(original_hwnd):
            win32gui.ShowWindow(original_hwnd, win32con.SW_SHOW)
            win32gui.SetForegroundWindow(original_hwnd)

        # 完了はバックグラウンドで待機（必要な場合）
        self.wait_until_finished()

    def close(self):
        """VOICEROID2 を閉じる"""
        if self.window:
            self.window.close()
