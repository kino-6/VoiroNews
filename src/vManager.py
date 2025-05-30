import subprocess
import json


class vManager:
    def __init__(self, exe_path):
        self.exe_path = exe_path
        self.args = {}

    def set_args(self, args):
        self.args.update(args)

    def load_args(self, setting_json):
        with open(setting_json, "r", encoding="UTF-8") as f:
            self.args.update(json.load(f))

    def generate_args(self, args):
        args_str = ""

        for k, v in args.items():
            args_str += str(k) + " " + str(v) + " "

        return args_str

    def call_exe(self, *args):
        cmd = self.exe_path

        for arg in args:
            cmd += " " + str(arg)

        print(cmd)
        return subprocess.Popen(cmd, shell=True)

    def main(self):
        args = self.generate_args(self.args)
        self.call_exe(args)
