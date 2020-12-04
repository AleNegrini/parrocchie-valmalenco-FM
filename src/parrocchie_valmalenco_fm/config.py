import os
import configparser
from urllib.error import URLError, HTTPError
from urllib.request import urlopen

from typing import List

DEFAULT_CONFIG_FOLDERS_SEARCH = ['../../resources', '../resources', 'resources']


class Config:

    def __init__(self, folders=DEFAULT_CONFIG_FOLDERS_SEARCH):
        self.config_folders = folders

    def config_check(self, file_names: List[str]):
        """
        Check the presence of the specified config files and return the path for each given file name
        i.e.
        input: "config.ini"
        return:
        {
            "config.ini": "../resources/config.ini"
        }
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

    def get_relay_ip(self, file_path: str):
        """
        Return the relay ip for the given relay configuration file
        """
        config = configparser.ConfigParser()
        config.read(file_path)

        ip = config['relay']['relay_ip']
        print("Relay ip is: {}".format(ip))

        return ip

    @staticmethod
    def get_streaming_url(ip, port):
        """
        Return the url from which the stream will be listened
        Args:
            ip: cam IP address
            port: cam PORT
        """
        return 'http://' + ip + ":" + port

    @staticmethod
    def is_reachable(url, timeout=5):
        """
        It checks whether a URL is reachable and returns values accordingly
        Args:
            url: url to test
            timeout: timeout seconds
        Returns:
            It returns a boolean value. True if the URL is reachable, False otherwise.
        """
        try:
            response_code = urlopen(url, timeout=timeout).getcode()
            print(response_code)
            return True
        except (HTTPError, URLError) as e:
            print(url + " is unreachable")
            return False
