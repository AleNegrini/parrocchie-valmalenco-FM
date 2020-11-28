import configparser


class CameraConfig:
    """
    Constant class definition: it contains all the IP, port, admin and pwd configuration regarding the IP cam
    """

    def __init__(self, file_path):
        config = configparser.ConfigParser()
        config.read(file_path)

        self.ip_dict = {}
        self.port_dict = {}
        self.user_dict = {}
        self.pass_dict = {}

        # parsing config file and generating the dictionaries for each metric
        # ex. ip_dict = {'caspoggio':'xxx.yyy.zzz.www', 'lanzada':'zzz.qqq.xxx.yyy'}
        for section in config.sections():
            self.ip_dict[section] = config.items(section)[0][1]
            self.port_dict[section] = config.items(section)[1][1]
            self.user_dict[section] = config.items(section)[2][1]
            self.pass_dict[section] = config.items(section)[3][1]

