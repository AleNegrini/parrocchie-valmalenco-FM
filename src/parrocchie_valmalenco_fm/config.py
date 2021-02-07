import os
import configparser
from ping3 import ping

from typing import List

DEFAULT_CONFIG_FOLDERS_SEARCH = ['../../resources', '../resources', 'resources']
DEFAULT_CONFIG_AUDIO_FOLDERS_SEARCH = ['../../resources/audio', '../resources/audio', 'resources/audio']


class Config:

    def __init__(self, folders=DEFAULT_CONFIG_FOLDERS_SEARCH, audio_folders=DEFAULT_CONFIG_AUDIO_FOLDERS_SEARCH):
        self.config_folders = folders
        self.audio_folders = audio_folders

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

    def sigla_check(self, sigla_list=['caspoggio_inizio.mp3',
                                      'caspoggio_fine.mp3',
                                      'lanzada_inizio.mp3',
                                      'lanzada_fine.mp3',
                                      'chiesa_vco_inizio.mp3',
                                      'chiesa_vco_fine.mp3',
                                      'spriana_inizio.mp3',
                                      'spriana_fine.mp3',
                                      'primolo_inizio.mp3',
                                      'primolo_fine.mp3',
                                      'torre_inizio.mp3',
                                      'torre_fine.mp3'
                                      ]):
        """
        Checks the presence of the specified sigla audio (both start and end)
        Args:
            sigla_list: list of mp3 audio file

        Returns:
            {
                "caspoggio_fine.mp3": "../resources/audio/caspoggio_fine.mp3"
            }
        """
        path_dict = {}

        for audio_path in sigla_list:
            path_dict[audio_path] = None

        for folder in self.audio_folders:
            for file_name in sigla_list:
                if os.path.exists(os.path.join(folder, file_name)):
                    print("Using {} in folder {}".format(file_name, folder))
                    path_dict[file_name] = os.path.join(folder, file_name)

        for key, value in path_dict.items():
            if not value:
                print("ERROR: File {} not found in {}.".format(key, self.config_folders))
                exit(1)

        print("Audio list check - PASSED.")
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
    def check_ping(url):
        """
        It checks whether a URL is reachable and returns values accordingly
        Args:
            url: url to test
            timeout: timeout seconds
        Returns:
            It returns a boolean value. True if the URL is reachable, False otherwise.
        """

        response = ping(url)
        if response is None:
            print(url + " ping failed")
            return False
        else:
            print(url + " ping successfull")
            return True
