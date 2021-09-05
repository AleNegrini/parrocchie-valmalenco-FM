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
            'lastPing': False,
            'nUP': 0,
            'nDOWN': 0,
            'pingExceptions': 0
        }
        yield {
            'id': 'another_node_1',
            'address': '192.168.53.1',
            'lastPing': False,
            'nUP': 0,
            'nDOWN': 0,
            'pingExceptions': 0
        }
        yield {
            'id': 'another_node_2',
            'address': '192.168.53.23',
            'lastPing': False,
            'nUP': 0,
            'nDOWN': 0,
            'pingExceptions': 0
        }
        yield {
            'id': 'another_node_3',
            'address': '192.168.53.24',
            'lastPing': False,
            'nUP': 0,
            'nDOWN': 0,
            'pingExceptions': 0
        }
        yield {
            'id': 'another_node_4',
            'address': '192.168.53.147',
            'lastPing': False,
            'nUP': 0,
            'nDOWN': 0,
            'pingExceptions': 0
        }

    def __get_nodes(self):  # private method
        for section, address in self.ip_dict.items():
            yield {
                'id': section,
                'address': address,
                'lastPing': False,
                'nUP': 0,
                'nDOWN': 0,
                'pingExceptions': 0
            }

    @staticmethod
    def ping_and_log(node, logging):
        node_id = node['id']
        address = node['address']
        logging.info('Ping thread on node ' + node_id + ' (' + address + ') started')

        while True:
            try:
                ret = ping(dest_addr=address, timeout=3)
                if ret is None:
                    new_ping = False
                else:
                    new_ping = True

                old_ping = node['lastPing']

                # UP/DOWN log
                if not old_ping and new_ping:
                    node['nUP'] += 1
                    logging.info("+++++ {} UP +++++ (nUp={},nDown={},pingExceptions={})".format(node_id, node['nUP'], node['nDOWN'], node['pingExceptions']))
                if old_ping and not new_ping:
                    node['nDOWN'] += 1
                    logging.info("----- {} DOWN ----- (nUp={},nDown={},pingExceptions={})".format(node_id, node['nUP'], node['nDOWN'], node['pingExceptions']))

                node['lastPing'] = new_ping

            except ping.EXCEPTIONS:
                node['pingExceptions'] += 1
                logging.info("***** {} PING EXCEPTION ***** (nUp={},nDown={},pingExceptions={})".format(node_id, node['nUP'], node['nDOWN'], node['pingExceptions']))

            time.sleep(3)

    def start_ping_test_threads(self, logging):
        logging.info("Starting ping test threads")
        for no in self.__get_nodes():
            x = threading.Thread(target=CameraConfig.ping_and_log, args=(no, logging))
            x.start()

    @staticmethod
    def fake_start_ping_test_threads(logging):
        logging.info("Starting FAKE ping test threads")
        for no in CameraConfig.get_fake_nodes():
            x = threading.Thread(target=CameraConfig.ping_and_log, args=(no, logging))
            x.start()