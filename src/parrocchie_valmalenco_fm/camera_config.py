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
            'nDOWN': 0
        }
        yield {
            'id': 'another_node_1',
            'address': '192.168.53.1',
            'lastPing': False,
            'nUP': 0,
            'nDOWN': 0
        }
        yield {
            'id': 'another_node_2',
            'address': '192.168.53.23',
            'lastPing': False,
            'nUP': 0,
            'nDOWN': 0
        }
        yield {
            'id': 'another_node_3',
            'address': '192.168.53.24',
            'lastPing': False,
            'nUP': 0,
            'nDOWN': 0
        }
        yield {
            'id': 'another_node_4',
            'address': '192.168.53.147',
            'lastPing': False,
            'nUP': 0,
            'nDOWN': 0
        }

    def __get_nodes(self):  # private method
        for section, address in self.ip_dict.items():
            yield {
                'id': section,
                'address': address,
                'lastPing': False,
                'nUP': 0,
                'nDOWN': 0
            }

    @staticmethod
    def ping_and_log(node, logging, report_interval):
        node_id = node['id']
        address = node['address']
        logging.info('Ping thread on node ' + node_id + ' (' + address + ') started')
        last_report_time = time.time()

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

            # UP/DOWN log
            if not old_ping and new_ping:
                node['nUP'] += 1
                logging.info(node_id + ' UP')
            if old_ping and not new_ping:
                node['nDOWN'] += 1
                logging.info(node_id + ' DOWN')

            # UP/DOWN count report
            current_time = time.time()
            if current_time - last_report_time > report_interval:
                logging.info('Report: ' + node_id + ' nDOWN = ' + str(node['nDOWN']) + ' nUP = ' + str(node['nUP']))
                last_report_time = current_time

            node['lastPing'] = new_ping
            time.sleep(3)

    def start_ping_test_threads(self, logging, report_interval):
        logging.info("Starting ping test threads")
        for no in self.__get_nodes():  # comment for testing offline
            x = threading.Thread(target=CameraConfig.ping_and_log, args=(no, logging, report_interval))
            x.start()

    @staticmethod
    def fake_start_ping_test_threads(logging, report_interval):
        logging.info("Starting FAKE ping test threads")
        for no in CameraConfig.get_fake_nodes():
            x = threading.Thread(target=CameraConfig.ping_and_log, args=(no, logging, report_interval))
            x.start()