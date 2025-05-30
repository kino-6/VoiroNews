import io
import contextlib
import os
import time
from datetime import datetime
from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError


class VoiceroidUIDumper:
    def __init__(self, app_title="VOICEROID2"):
        self.app_title = app_title
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.dump_dir = "voiceroid_ui_dump"
        os.makedirs(self.dump_dir, exist_ok=True)

    def connect(self):
        print(f"[✅] Connecting to {self.app_title}...")
        self.app = Application(backend="uia").connect(title_re=self.app_title)
        self.window = self.app.window(title_re=self.app_title)
        print(f"[✅] Connected to main {self.app_title} window: {self.window.window_text()}")

    def find_tab_controls(self):
        # Tabが複数あるので、すべて取得して返す
        return [
            ctrl for ctrl in self.window.children() if ctrl.friendly_class_name() == "TabControl"
        ]

    def dump_controls(self, tab_name):
        try:
            file_path = os.path.join(self.dump_dir, f"{self.timestamp}_{tab_name}.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                with io.StringIO() as buf, contextlib.redirect_stdout(buf):
                    self.window.print_control_identifiers()
                    output = buf.getvalue()
                    f.write(output)
            print(f"[💾] Dumped controls under tab '{tab_name}' to {file_path}")
        except Exception as e:
            print(f"[❌] Failed to dump tab '{tab_name}': {e}")

    def dump_comboboxes(self):
        print(f"[🔍] Dumping ComboBoxes in main window...")
        try:
            comboboxes = self.window.descendants(control_type="ComboBox")
            dump_path = os.path.join(self.dump_dir, f"{self.timestamp}_main_comboboxes.txt")
            with open(dump_path, "w", encoding="utf-8") as f:
                for i, cb in enumerate(comboboxes, 1):
                    try:
                        name = cb.window_text()
                        items = cb.texts()
                        f.write(f"[{i}] ComboBox: {name}\n")
                        f.write(f"    Items: {items}\n")
                    except Exception as cb_err:
                        f.write(f"[{i}] ComboBox: <Error reading>\n")
                        f.write(f"    Error: {cb_err}\n")
            print(f"[📦] Dumped ComboBox list to {dump_path}")
        except Exception as e:
            print(f"[❌] Failed to dump comboboxes: {e}")

    def dump_tabs(self):
        tab_controls = self.find_tab_controls()
        if not tab_controls:
            print("[❌] No TabControl found.")
            return

        for tab_control in tab_controls:
            try:
                tab_names = tab_control.texts()
                print(f"[📌] Found {len(tab_names)} tabs")
                for tab_name in tab_names:
                    print(f"[🔁] Selecting tab: {tab_name}")
                    try:
                        tab_control.select(tab_name)
                        time.sleep(0.5)
                        self.dump_controls(tab_name)
                    except Exception as e:
                        print(f"[❌] Failed to select tab '{tab_name}': {e}")
            except Exception as e:
                print(f"[❌] Failed to enumerate tabs: {e}")

        self.dump_comboboxes()


if __name__ == "__main__":
    try:
        dumper = VoiceroidUIDumper()
        dumper.connect()
        dumper.dump_tabs()
    except ElementNotFoundError:
        print("[❌] VOICEROID2 window not found. Is it running?")
    except Exception as e:
        print(f"[❌] Unexpected error: {e}")
