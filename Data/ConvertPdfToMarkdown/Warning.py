import sys

_warning_mode = False


def set_warning_mode(enabled: bool):
    global _warning_mode
    _warning_mode = enabled


def Warning(message: str):
    if _warning_mode:
        print("Warning:", message)


def WarnAndExit(message: str):
    print(message)
    print("Exiting.")
    sys.exit()
