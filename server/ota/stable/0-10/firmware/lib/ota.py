# Standard OTA lib
import os
import json
import requests


class OTA:
    def __init__(self, config):
        """OTA object"""
        self.branch = config.branch
        self.server_url = config.server_url

    def check(self):
        """Checks for update"""
        versions_path = self.server_url + '/server/ota/versions.json'
        if self.__ping__(self.server_url):
            content = self.__download_content__(versions_path)
            if content:
                try:
                    data = json.loads(content)
                    with open("/flash/current_version", "r") as f:
                        ver = f.read()
                    if data[self.branch] == ver:
                        return False
                    else:
                        return data[self.branch]
                except BaseException as e:
                    return False

        else:
            return False

    def __backup__(self):
        """Backup firmware"""
        try:
            # Define paths
            path = '/flash/'
            backup_folder = path + "_backup_"
            try:
                os.mkdir(backup_folder)  # Try to create folder
            except BaseException as e:
                pass
            all_files = os.listdir('/flash')  # Get list of all files and folders
            try:
                all_files.remove("_backup_")  # Remove backup folder from filelist
                all_files.remove("config.py")  # Remove config file from filelist
            except BaseException as e:
                return False
            for file in all_files:
                try:  # Check for folder
                    new = path + file + '/'  # Define path to folder
                    backup_path = backup_folder + '/' + file  # Define path to folder in backup_folder
                    alf = os.listdir(path + file)  # Get list of all files in folder
                    # or Handle Exception if it is path to file
                    try:
                        os.mkdir(backup_path)  # Try to create dir in backup folder
                    except BaseException as e:
                        pass
                    for f in alf:  # For every file in this dir, we move this file
                        try:
                            os.rename(new + f, backup_path + '/' + f)
                        except BaseException:
                            os.remove(backup_path + '/' + f)  # Remove old backup
                            os.rename(new + f, backup_path + '/' + f)  # Move in backup
                except BaseException as e:  # If it is file
                    try:
                        os.rename(path + file, backup_folder + '/' + file)  # Move this file
                    except BaseException as e:
                        os.remove(backup_folder + '/' + file)  # Remove this file in backup
                        os.rename(path + file, backup_folder + '/' + file)  # Again try to move
            return True
        except BaseException as E:
            return False

    def update(self, new_version):
        """Update"""
        print("update", new_version)
        version_url = self.server_url + '/server/ota/{}/{}'.format(self.branch, new_version)
        firmware_url = version_url + '/firmware/'
        files_url = version_url + "/files.json"
        if self.__ping__(self.server_url):
            stat = self.__backup__()
            if stat:
                content = self.__download_content__(files_url)
                if content:
                    try:
                        js = json.loads(content)
                        urls = js['files']
                        dirs = js['dirs']
                        for dir in dirs:
                            try:
                                data = os.listdir(dir)
                            except BaseException as e:
                                try:
                                    os.mkdir(dir)
                                except BaseException as e:
                                    pass
                        for url in urls:
                            filepath = url.replace(firmware_url, '/flash/')
                            content = self.__download_content__(url)
                            if content:
                                with open(filepath, 'w') as f:
                                    f.write(content)
                            else:
                                self.__restore__()
                                return False
                        return True
                    except BaseException as e:
                        return False

        else:
            return False

    def __restore__(self):
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
                    except BaseException as e:
                        pass
                    for file2 in bkp_filelist_f2:  # For every file in this dir, we move this file
                        path_2 = backup_filepath+'/'+file2
                        org_path_2 = original_filepath+'/'+file2
                        try:
                            os.rename(path_2, org_path_2)
                        except BaseException as g:
                            os.remove(org_path_2)  # Remove new corrupted file
                            os.rename(path_2, org_path_2)  # Move from backup
                except BaseException as e:  # If it is file
                    try:
                        os.rename(backup_filepath, original_filepath)  # Move this file
                    except BaseException as e:
                        os.remove(original_filepath)  # Remove new corrupted file
                        os.rename(backup_filepath, original_filepath)   # Again try to move
            return True
        except BaseException as E:
            return False

    def __download_content__(self, url):
        """downloads file content"""
        try:
            print("download", url)
            request = requests.get(url)
            if request[0] is 200:
                return request[2]
            else:
                return False
        except BaseException as e:
            return False

    def __ping__(self, url):
        """Send get request to specified url."""
        try:
            print("ping", url)
            request = requests.get(url)
            if request[0] is 200:
                return True
            else:
                return True
        except BaseException as e:
            return False
