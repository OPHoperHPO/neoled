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
        versions_path = self.server_url+'/server/ota/versions.json'
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
        try:
            path = '/flash/'
            backup_folder = path+"_backup_"
            try:
                os.mkdir(backup_folder)
            except BaseException as e:
                pass
            all_files = os.listdir(path)
            try:
                all_files.remove("_backup_")
                all_files.remove("config.py")
            except BaseException as e:
                pass
            for file in all_files:
                try:
                    new = path+file+'/'
                    backup_path = backup_folder+'/'+file
                    alf = os.listdir(new)
                    os.mkdir(backup_path)
                    for f in alf:
                        os.rename(new+f, backup_path+'/'+f)
                except BaseException as e:
                    os.rename(path+file, backup_folder+'/'+file)
            return True
        except BaseException as E:
            return False

    def update(self, new_version):
        """Update"""
        print("update", new_version)
        version_url = self.server_url+'/server/ota/{}/{}'.format(self.branch, new_version)
        firmware_url = version_url+'/firmware/'
        files_url = version_url+"/files.json"
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
        try:
            path = '/flash/'
            backup_folder = path + "_backup_"
            all_files = os.listdir(backup_folder)
            try:
                all_files.remove("_backup_")
                all_files.remove("config.py")
            except BaseException as e:
                pass
            for file in all_files:
                try:
                    new = backup_folder+'/'+ file + '/'
                    backup_path = path + file
                    alf = os.listdir(new)
                    try:
                        os.mkdir(backup_path)
                    except BaseException as e:
                        pass
                    for f in alf:
                        os.rename(new + f, backup_path + '/' + f)
                except BaseException as e:
                    os.rename(backup_folder+'/' + file, path + file)
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
