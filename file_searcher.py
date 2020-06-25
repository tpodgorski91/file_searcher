from pathlib import Path, PurePath
import platform
from typing import List
import subprocess


def list_drives():
    system_name = platform.system()

    method = {
        "Linux": list_drives_linux,
        "Darwin": list_drives_macos,
        "Windows": list_drives_windows,
    }[system_name]

    drives = method()
    return drives


def list_drives_linux() -> List[str]:
    # TODO: find out how to return
    return []


def list_drives_macos() -> List[str]:
    import psutil
    return [
        partition.device for partition in psutil.disk_partitions()
    ]


def list_drives_windows() -> List[str]:
    import string
    from ctypes import windll

    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives


def get_file(drive, name):
    """

    :param drive:
    :param name:
    :return:
    """
    file_path = sorted(Path(f"{drive}:/").glob(f"*/*{name}*"))
    file_path = str(file_path)
    if platform.system() == 'Windows':
        file_path = file_path[14:-3]
    else:
        file_path = file_path[11:-3]
    return file_path

# TODO: how to open file contains a text on different OS?


if __name__ == '__main__':

    print("Please type from the list above drive where file is stored")
    user_drive = input()
    print("Please provide either entire or some portion of file name")
    file_name = input()
    subprocess.call([r'notepad.exe', get_file(user_drive, file_name)])
