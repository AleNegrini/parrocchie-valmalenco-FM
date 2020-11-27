import configparser


class Constants:
    """
    Constant class definition: it contains all the constants values to be used throughout the entire script
    """
    config = configparser.ConfigParser()
    config.read('../resources/config.ini')

    ip_dict = {}
    port_dict = {}
    channel_dict = {}
    user_dict = {}
    pass_dict = {}

    # parsing config file and generating the dictionaries for each metric
    # ex. ip_dict = {'caspoggio':'xxx.yyy.zzz.www', 'lanzada':'zzz.qqq.xxx.yyy'}
    for section in config.sections():
        ip_dict[section] = config.items(section)[0][1]
        port_dict[section] = config.items(section)[1][1]
        #channel_dict[section] = config.items(section)[2][1]
        user_dict[section] = config.items(section)[2][1]
        pass_dict[section] = config.items(section)[3][1]

