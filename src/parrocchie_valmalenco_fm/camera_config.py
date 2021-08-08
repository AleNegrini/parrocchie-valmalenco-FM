import configparser
import time
import threading
from ping3 import ping


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

    @staticmethod
    def get_fake_nodes():
        yield {
            'id': 'home',
            'address': '127.0.0.1',
            'lastPing': False
        }
        yield {
            'id': 'another_node',
            'address': '192.168.53.23',
            'lastPing': False
        }

    def __get_nodes(self):  # private method
        for section, address in self.ip_dict.items():
            yield {
                'id': section,
                'address': address,
                'lastPing': False
            }

    @staticmethod
    def ping_and_log(node, logging):
        node_id = node['id']
        address = node['address']
        logging.info('Ping thread on node ' + node_id + ' (' + address + ') started')
        while True:
            old_ping = node['lastPing']

            try:
                ret = ping(dest_addr=address, timeout=3)
                if ret is None:
                    new_ping = False
                else:
                    new_ping = True
            except ping.EXCEPTIONS:
                new_ping = False

            if not old_ping and new_ping:
                logging.info('Node ' + node_id + ' goes UP')
            if old_ping and not new_ping:
                logging.info('Node ' + node_id + ' goes DOWN')

            node['lastPing'] = new_ping
            time.sleep(3)

    def start_ping_test_threads(self, logging):
        logging.info("Starting ping test threads")
        # for no in CameraConfig.get_fake_nodes():  # uncomment for testing offline
        for no in self.__get_nodes():  # comment for testing offline
            x = threading.Thread(target=CameraConfig.ping_and_log, args=(no, logging))
            x.start()
