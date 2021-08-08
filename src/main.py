import time
import sys
import requests
import subprocess
import logging
import threading

from ping3 import ping

from parrocchie_valmalenco_fm.utils import get_current_date, get_current_time
from parrocchie_valmalenco_fm.orari_config import OrariConfig
from parrocchie_valmalenco_fm.config import Config
from parrocchie_valmalenco_fm.camera_config import CameraConfig

ORARI_FILE = 'orari.csv'
RELAY_CONFIG_FILE = 'config-relay.ini'
CAMERA_CONFIG_FILE = 'config.ini'

nodes = {
    'home': {
        'address': '127.0.0.1',
        'lastPing': False
    },
    'another_node': {
        'address': '192.168.53.23',
        'lastPing': False
    }
}


def background_ping(ping_id):
    logging.info('Ping thread on node ' + ping_id + ' started')
    while True:
        address = nodes[ping_id]['address']
        old_ping = nodes[ping_id]['lastPing']

        try:
            ret = ping(dest_addr=address, timeout=3)
            if ret is None:
                new_ping = False
            else:
                new_ping = True
        except ping.EXCEPTIONS:
            new_ping = False

        if not old_ping and new_ping:
            logging.info('Node ' + ping_id + ' goes UP')
        if old_ping and not new_ping:
            logging.info('Node ' + ping_id + ' goes DOWN')

        nodes[ping_id]['lastPing'] = new_ping
        time.sleep(3)


if __name__ == '__main__':

    # validate the presence of required config files
    config = Config()
    config_path_dict = config.config_check([ORARI_FILE, RELAY_CONFIG_FILE, CAMERA_CONFIG_FILE])

    cameras = CameraConfig(config_path_dict[CAMERA_CONFIG_FILE])
    relay_ip = config.get_relay_ip(config_path_dict[RELAY_CONFIG_FILE])
    relay_block_ip = '192.168.1.200'
    orari_config = OrariConfig(config_path_dict[ORARI_FILE])

    sigla_path_dict = config.sigla_check()

    pid_vlc = None
    streaming_started = False

    # logging settings
    logging.basicConfig(filename='app.log', level=logging.DEBUG, filemode='a', format='%(asctime)s - %(message)s')

    logging.info('Program started')

    # to start the ping threads:
    # pythonw main.py random_string
    # watch the last lines of the log:
    # tail -n 15 -F app.log
    if len(sys.argv) > 1:
        logging.info("Starting ping test threads")
        for node_id in nodes.keys():
            x = threading.Thread(target=background_ping, args=(node_id,))
            x.start()

    while True:
        current_date = get_current_date()
        current_time = get_current_time()
        calendar = orari_config.read_file()
        active_slot = calendar.active_slot(current_date, current_time)

        # START EVENT: if there is an active slot
        if active_slot is not None:

            # build the streaming url
            url = Config.get_streaming_url(cameras.ip_dict[active_slot], cameras.port_dict[active_slot])
            path_audio_start = sigla_path_dict[active_slot + '_inizio.mp3']
            path_audio_end = sigla_path_dict[active_slot + '_fine.mp3']

            # the url is now eligible to be started. However, until the endpoint is not reachable, it can't be started
            if Config.check_ping(cameras.ip_dict[active_slot]) and not streaming_started:

                # 1° Step: trigger the relays
                r = requests.post('http://' + relay_ip + '/relays.cgi?relay=1')
                try:
                    r1 = requests.get('http://' + relay_block_ip + '/3000/01')
                    time.sleep(1)
                    logging.info('Relay Block n_1 @' + relay_block_ip + ' start success')
                except:
                    logging.info('Relay Block n_1 @' + relay_block_ip + ' start failed')
                    pass

                try:
                    r2 = requests.get('http://' + relay_block_ip + '/3000/03')
                    time.sleep(1)
                    logging.info('Relay Block n_2 @' + relay_block_ip + ' start success')
                except:
                    logging.info('Relay Block n_2 @' + relay_block_ip + ' start failed')
                    pass

                logging.info('Relay @' + relay_ip + ' triggered')

                time.sleep(2)

                if sys.platform != 'darwin':

                    # 2° Step: play the start event announcement
                    proc = subprocess.Popen(['powershell.exe', "C:/'Program Files'/VideoLAN/VLC/vlc.exe "
                                             + path_audio_start + ' vlc://quit'], stdout=sys.stdout)
                    time.sleep(15)
                    logging.info('Playing ' + path_audio_start)

                    # 3° Step: play the stream
                    proc = subprocess.Popen(['powershell.exe',
                                             "C:/'Program Files'/VideoLAN/VLC/vlc.exe " + url +
                                             " --novideo"], stdout=sys.stdout)
                else:

                    # 2° Step: play the start event announcement
                    proc = subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC ' + path_audio_start +
                                             ' vlc://quit'], shell=True)
                    time.sleep(15)
                    logging.info('Playing ' + path_audio_start)

                    # 3° Step: play the stream
                    proc = subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC ' + url +
                                             " --novideo"], shell=True)

                logging.info("Started listening from " + url + " at " + current_time)
                logging.info("Started listening from " + url + " at " + current_time)
                pid_vlc = proc.pid
                streaming_started = True

            if not Config.check_ping(cameras.ip_dict[active_slot]) and streaming_started:
                if sys.platform != 'darwin':
                    # 1° Step: stop the stream
                    subprocess.Popen(['powershell.exe', 'Stop-Process -name vlc -Force'], shell=True)
                    time.sleep(5)

                    # 2° Step: play the stop event announcement
                    proc = subprocess.Popen(["powershell.exe", "C:/'Program Files'/VideoLAN/VLC/vlc.exe "
                                             + path_audio_end + " vlc://quit"], shell=True)

                    logging.info('Playing ' + path_audio_end)

                else:
                    # 1° Step: stop the stream
                    subprocess.Popen(['kill -9 ' + str(pid_vlc)], shell=True)
                    time.sleep(5)

                    # 2° Step: play the stop event announcement
                    subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC ' + path_audio_end +
                                      ' vlc://quit'], shell=True)

                    logging.info('Playing ' + path_audio_end)

                time.sleep(15)
                r = requests.post('http://' + relay_ip + '/relays.cgi?relay=1')
                try:
                    r1 = requests.get('http://' + relay_block_ip + '/3000/00')
                    time.sleep(1)
                    logging.info('Relay Block n_1 @' + relay_block_ip + ' stop success')
                except:
                    logging.info('Relay Block n_1 @' + relay_block_ip + ' stop failed')
                    pass

                try:
                    r2 = requests.get('http://' + relay_block_ip + '/3000/02')
                    time.sleep(1)
                    logging.info('Relay Block n_2 @' + relay_block_ip + ' stop success')
                except:
                    logging.info('Relay Block n_2 @' + relay_block_ip + ' stop failed')
                    pass

                logging.info("Stopped " + url + " at " + current_time + " due to the mic unreachability")
                pid_vlc = None
                streaming_started = False

        # STOP EVENT
        if active_slot is None and streaming_started:
            if sys.platform != 'darwin':
                # 1° Step: stop the stream
                subprocess.Popen(['powershell.exe', 'Stop-Process -name vlc -Force'], shell=True)
                time.sleep(5)

                # 2° Step: play the stop event announcement
                subprocess.Popen(["powershell.exe", "C:/'Program Files'/VideoLAN/VLC/vlc.exe "
                                  + path_audio_end + " vlc://quit"], shell=True)

                logging.info('Playing ' + path_audio_end)

            else:
                # 1° Step: stop the stream
                subprocess.Popen(['kill -9 ' + str(pid_vlc)], shell=True)
                time.sleep(5)

                # 2° Step: play the stop event announcement
                proc = subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC ' + path_audio_end +
                                         ' vlc://quit'], shell=True)
                logging.info('Playing ' + path_audio_end)

            time.sleep(15)
            r = requests.post('http://' + relay_ip + '/relays.cgi?relay=1')

            try:
                r1 = requests.get('http://' + relay_block_ip + '/3000/00')
                logging.info('Relay Block n_1 @' + relay_block_ip + ' stop success')
                time.sleep(1)
            except:
                logging.info('Relay Block n_1 @' + relay_block_ip + ' stop failed')
                pass
            try:
                r2 = requests.get('http://' + relay_block_ip + '/3000/02')
                time.sleep(1)
                logging.info('Relay Block n_2 @' + relay_block_ip + ' stop success')
            except:
                logging.info('Relay Block n_2 @' + relay_block_ip + ' stop failed')
                pass
            logging.info("Stopped " + url + " at " + current_time + " due to timeout expiration")
            pid_vlc = None
            streaming_started = False
            last_slot = None

        time.sleep(60)
