# logger.py
# MZ/X – Egységes logolási rendszer színes kimenettel

import datetime

class Log:

    @staticmethod
    def _ts():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def info(msg):
        print(f"\033[94m[INFO] {Log._ts()} | {msg}\033[0m")

    @staticmethod
    def warn(msg):
        print(f"\033[93m[WARN] {Log._ts()} | {msg}\033[0m")

    @staticmethod
    def error(msg):
        print(f"\033[91m[ERROR] {Log._ts()} | {msg}\033[0m")

    @staticmethod
    def ws(msg):
        print(f"\033[96m[WS] {Log._ts()} | {msg}\033[0m")

    @staticmethod
    def ai(msg):
        print(f"\033[95m[AI] {Log._ts()} | {msg}\033[0m")
