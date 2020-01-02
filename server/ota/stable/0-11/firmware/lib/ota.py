# Standard OTA lib
# Developed by Anodev Development (OPHoperHPO) (https://github.com/OPHoperHPO)
import os
import json
import machine
import requests


# noinspection PyBroadException,PyUnresolvedReferences
class OTA:
    def __init__(self, config):
        """OTA object"""
        # Init vars
        self.branch = config.branch
        self.server_url = config.server_url
        self.old_ver = "0-00"

    def check(self):
        """Checks for update"""
        print("OTA check")
        versions_path = self.server_url + '/server/ota/versions.json' # Make url
        if self.__ping__(self.server_url): # Ping server
            content = self.__download_content__(versions_path)  # Download versions in branch
            if content:
                try:
                    data = json.loads(content)
                    with open("/flash/current_version", "r") as f:
                        ver = f.read()
                        self.old_ver = ver
                    if data[self.branch] == ver: # Compare versions
                        return False
                    else:
                        return data[self.branch]
                except BaseException:
                    return False

        else:
            return False

    @staticmethod
    def __backup__():
        """Backup firmware"""
        print("Backup start")
        try:
            # Define paths
            path = '/flash/'
            backup_folder = path + "_backup_"
            try:
                os.mkdir(backup_folder)  # Try to create folder
            except BaseException:
                pass
            all_files = os.listdir('/flash')  # Get list of all files and folders
            try:
                all_files.remove("_backup_")  # Remove backup folder from filelist
                all_files.remove("config.py")  # Remove config file from filelist
            except BaseException:
                return False
            for file in all_files:
                try:  # Check for folder
                    new = path + file + '/'  # Define path to folder
                    backup_path = backup_folder + '/' + file  # Define path to folder in backup_folder
                    alf = os.listdir(path + file)  # Get list of all files in folder
                    # or Handle Exception if it is path to file
                    try:
                        os.mkdir(backup_path)  # Try to create dir in backup folder
                    except BaseException:
                        pass
                    for f in alf:  # For every file in this dir, we move this file
                        try:
                            os.rename(new + f, backup_path + '/' + f)
                        except BaseException:
                            os.remove(backup_path + '/' + f)  # Remove old backup file
                            os.rename(new + f, backup_path + '/' + f)  # Move file in backup
                except BaseException:  # If it is file
                    try:
                        os.rename(path + file, backup_folder + '/' + file)  # Move this file
                    except BaseException:
                        os.remove(backup_folder + '/' + file)  # Remove this file in backup folder
                        os.rename(path + file, backup_folder + '/' + file)  # Again try to move
            print("Backup finished")
            return True
        except BaseException:
            print("Backup error")
            return False

    def update(self, new_version):
        """Update"""
        print("Update to", new_version, "from", self.old_ver)
        # Make urls
        version_url = self.server_url + '/server/ota/{}/{}'.format(self.branch, new_version)
        firmware_url = version_url + '/firmware/'
        files_url = version_url + "/files.json"
        if self.__ping__(self.server_url): # Ping server
            stat = self.__backup__() # Backup old firmware
            if stat:
                print("Update started")
                content = self.__download_content__(files_url)  # Download files and dirs paths from files.json
                if content:
                    try:
                        js = json.loads(content)
                        urls = js['files']
                        dirs = js['dirs']
                        for dir_name in dirs: # Create dirs
                            try:
                                os.listdir(dir_name)
                            except BaseException:
                                try:
                                    os.mkdir(dir_name)
                                except BaseException:
                                    pass
                        for url in urls: # Download new firmware
                            filepath = url.replace(firmware_url, '/flash/')
                            content = self.__download_content__(url)
                            if content:
                                with open(filepath, 'w') as f:
                                    f.write(content)
                            else:
                                print("Update error. Start restore firmware")
                                self.__restore__() # Restore old firmware if error with new
                                print("Restore finished")
                                print("Reboot...")
                                machine.reset()  # Reboot after restore
                                return False
                        print("Update finished")
                        print("Reboot...")
                        machine.reset()  # Reboot after upgrade
                        return True
                    except BaseException:
                        return False

        else:
            return False

    @staticmethod
    def __restore__():
        """Restore firmware"""
        try:
            # Define paths
            path = '/flash'
            backup_folder = path + '/' + "_backup_"
            backup_filelist = os.listdir(backup_folder)  # Get list of all files and folders
            for file in backup_filelist:
                # Define paths
                backup_filepath = backup_folder + '/' + file
                original_filepath = path + '/' + file
                try:  # Check for folder
                    bkp_filelist_f2 = os.listdir(backup_filepath)  # Get list of all files in folder
                    # or Handle Exception if it is path to file
                    try:
                        os.mkdir(original_filepath)  # Try to create dir in path
                    except BaseException:
                        pass
                    for file2 in bkp_filelist_f2:  # For every file in this dir, we move this file
                        path_2 = backup_filepath + '/' + file2
                        org_path_2 = original_filepath + '/' + file2
                        try:
                            os.rename(path_2, org_path_2)
                        except BaseException:
                            os.remove(org_path_2)  # Remove new corrupted file
                            os.rename(path_2, org_path_2)  # Move from backup
                except BaseException:  # If it is file
                    try:
                        os.rename(backup_filepath, original_filepath)  # Move this file
                    except BaseException:
                        os.remove(original_filepath)  # Remove new corrupted file
                        os.rename(backup_filepath, original_filepath)  # Again try to move
            return True
        except BaseException:
            return False

    @staticmethod
    def __download_content__(url):
        """downloads file content"""
        try:
            print("download", url)
            request = requests.get(url)
            if request[0] is 200:
                return request[2]
            else:
                return False
        except BaseException:
            return False

    @staticmethod
    def __ping__(url):
        """Send get request to specified url."""
        try:
            print("ping", url)
            request = requests.get(url)
            if request[0] is 200:
                return True
            else:
                return True
        except BaseException:
            return False
