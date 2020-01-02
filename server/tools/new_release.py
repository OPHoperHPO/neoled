# Update maker tool
import os
import json
import shutil
from config_tools import OTA_Tools

TOOL = "stable"
SERVER_URL = OTA_Tools.server  # For files.json

def open_json(path: str):
    """Opens json"""
    with open(path, "r") as f:
        data = json.load(f)
    return data

def create_filelist(upd_path):
    """Creates files.json"""
    dirs_json = []
    files_json = []
    firmware_dir = os.path.join(upd_path, "firmware")
    for root, dirs, files in os.walk(firmware_dir):
        for file in files:
            files_json.append(os.path.join(root.replace("..", SERVER_URL), file))
        for dir in dirs:
            dirs_json.append(os.path.join(root.replace(firmware_dir, "/flash"), dir))
    files = {
        "files": files_json,
        "dirs": dirs_json
    }
    with open(os.path.join(upd_path, "files.json"), "w", encoding='utf-8') as f:
        json.dump(files, f, ensure_ascii=False, indent=4)


def main():
    """Makes new firmware version"""
    old_update = open_json("../ota/versions.json")[TOOL]
    update_version = input("Old version: {}\n"
                           "New update version: ".format(old_update))
    # Check for different OTA ver
    if old_update == update_version:
        print("Please type different versions for updates!")
        update_version = input("Old version: {}\n"
                               "New update version: ".format(old_update))
        if old_update == update_version:
            print("Relaunch program and write another update version!")
            exit(1)
    if os.path.exists(os.path.join("../ota/{}".format(TOOL), update_version)):
        print("UPDATE FOLDER EXISTS! PLEASE DELETE AND TRY AGAIN!")
        exit(1)
    try:
        update_path = os.path.join("../ota/{}".format(TOOL), update_version)
        firmware_path = os.path.join(update_path, "firmware")
        print("Create folders in {}".format(update_path))
        os.makedirs(update_path)
        print("Copy files from ../../ota_firmware to {}".format(update_path))
        shutil.copytree("../../ota_firmware", firmware_path)
        print("Create current_version file")
        with open(os.path.join(firmware_path, "current_version"), "w") as f:
            f.write(update_version)
        print("Create files.json in {}".format(update_path))
        create_filelist(update_path)
        print("Change version in version.json")
        old_versions = open_json("../ota/versions.json")
        old_versions[TOOL] = update_version
        with open("../ota/versions.json", "w", encoding='utf-8') as f:
            json.dump(old_versions, f, ensure_ascii=False, indent=4)
        print("Update created successfully!")
    except BaseException as e:
        print("Error! ", e)
        exit(1)


if __name__ == "__main__":
    main()
