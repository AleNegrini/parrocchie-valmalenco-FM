import time
import requests
import logging


class Relay:

    def __init__(self, relay_ip: str, relay_block_ip: str):
        self.relay_ip = relay_ip
        self.relay_block_ip = relay_block_ip

    def trigger(self, operation_type: str):
        r = requests.post('http://' + self.relay_ip + '/relays.cgi?relay=1')

        try:
            r1 = requests.get('http://' + self.relay_block_ip + '/3000/01')
            time.sleep(1)
            logging.info('Relay Block n_1 @%s %s success', self.relay_block_ip, operation_type)
        except:
            logging.info('Relay Block n_1 @%s %s failed', self.relay_block_ip, operation_type)
            pass

        try:
            r2 = requests.get('http://' + self.relay_block_ip + '/3000/03')
            time.sleep(1)
            logging.info('Relay Block n_2 @%s %s success', self.relay_block_ip, operation_type)
        except:
            logging.info('Relay Block n_2 @%s %s failed', self.relay_block_ip, operation_type)
            pass

        logging.info('Relay @%s triggered for %s', self.relay_ip, operation_type)
