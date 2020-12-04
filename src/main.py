import time
import sys
import requests
import subprocess
from parrocchie_valmalenco_fm.utils import get_current_date, get_current_time
from parrocchie_valmalenco_fm.orari_config import OrariConfig
from parrocchie_valmalenco_fm.config import Config
from parrocchie_valmalenco_fm.camera_config import CameraConfig

ORARI_FILE = 'orari.csv'
RELAY_CONFIG_FILE = 'config-relay.ini'
CAMERA_CONFIG_FILE = 'config.ini'

if __name__ == '__main__':

    # validate the presence of required config files
    config = Config()
    config_path_dict = config.config_check([ORARI_FILE, RELAY_CONFIG_FILE, CAMERA_CONFIG_FILE])

    cameras = CameraConfig(config_path_dict[CAMERA_CONFIG_FILE])
    relay_ip = config.get_relay_ip(config_path_dict[RELAY_CONFIG_FILE])
    orari_config = OrariConfig(config_path_dict[ORARI_FILE])

    pid_vlc = None
    streaming_started = False

    while True:
        current_date = get_current_date()
        current_time = get_current_time()
        calendar = orari_config.read_file()
        active_slot = calendar.active_slot(current_date, current_time)

        # START EVENT: if there is an active slot
        if active_slot is not None:

            # build the streaming url
            url = Config.get_streaming_url(cameras.ip_dict[active_slot], cameras.port_dict[active_slot])

            # the url is now eligible to be started. However, until the endpoint is not reachable, it can't be started
            if Config.is_reachable(url) and not streaming_started:
                if sys.platform != 'darwin':
                    proc = subprocess.Popen(['powershell.exe',
                                             "C:/'Program Files'/VideoLAN/VLC/vlc.exe " + url +
                                             " --novideo"], stdout=sys.stdout)
                else:
                    proc = subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC ' + url +
                                             " --novideo"], shell=True)

                r = requests.post('http://' + relay_ip + '/relays.cgi?relay=1')
                print("Started listening from "+url+" at "+current_time)
                pid_vlc = proc.pid
                streaming_started = True

            if not Config.is_reachable(url) and streaming_started:
                if sys.platform != 'darwin':
                    subprocess.Popen(['powershell.exe', 'Stop-Process -name vlc -Force'], shell=True)
                else:
                    subprocess.Popen(['kill -9 ' + str(pid_vlc)], shell=True)
                r = requests.post('http://' + relay_ip + '/relays.cgi?relay=1')
                print("Stopped " + url + " at " + current_time+" due to the mic unreachability")
                pid_vlc = None
                streaming_started = False

        if active_slot is None and streaming_started:
            #STOP EVENT
            if sys.platform != 'darwin':
                subprocess.Popen(['powershell.exe', 'Stop-Process -name vlc -Force'], shell=True)
            else:
                subprocess.Popen(['kill -9 ' + str(pid_vlc)], shell=True)
            # r = requests.post('http://' + relay_ip + '/relays.cgi?relay=1')
            print("Stopped " + url + " at " + current_time + " due to timeout expiration")
            pid_vlc = None
            streaming_started = False
            last_slot = None


        time.sleep(60)
