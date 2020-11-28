import os
import configparser

DEFAULT_CONFIG_FOLDERS_SEARCH = ['../resources', 'resources']


class Config:

    def __init__(self, folders=DEFAULT_CONFIG_FOLDERS_SEARCH):
        self.config_folders = folders

    def config_check(self, file_names):
        """
        Check the presence of the specified config files and return the location
        """
        path_dict = {}

        for file_name in file_names:
            path_dict[file_name] = None

        for folder in self.config_folders:
            for file_name in file_names:
                if os.path.exists(os.path.join(folder, file_name)):
                    print("Using {} in folder {}".format(file_name, folder))
                    path_dict[file_name] = os.path.join(folder, file_name)

        for key, value in path_dict.items():
            if not value:
                print("ERROR: File {} not found in {}.".format(key, self.config_folders))
                exit(1)

        print("Configuration check - PASSED.")
        return path_dict

    def get_relay_ip(self, file_path):
        config = configparser.ConfigParser()
        config.read(file_path)

        ip = config['relay']['relay_ip']
        print("Relay ip is: {}".format(ip))

        return ip

