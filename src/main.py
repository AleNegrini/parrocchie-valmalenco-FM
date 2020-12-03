import time
import sys
import subprocess
import requests
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

    last_slot = None
    pid_vlc = None
    while True:
        current_date = get_current_date()
        current_time = get_current_time()
        calendar = orari_config.read_file()
        active_slot = calendar.active_slot(current_date, current_time)

        if last_slot != active_slot and active_slot is not None:

            # build the rtsp link
            rtsp_link = "rtsp://" + \
                  cameras.user_dict[active_slot] + ":" + cameras.pass_dict[active_slot] + "@" + \
                  cameras.ip_dict[active_slot] + ":" + cameras.port_dict[active_slot]

            if sys.platform != 'darwin':
                proc = subprocess.Popen(['powershell.exe',
                                         "C:/'Program Files'/VideoLAN/VLC/vlc.exe " + rtsp_link +
                                         " --novideo --zoom=0.20"], stdout=sys.stdout)
            else:
                proc = subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC ' + rtsp_link +
                                         " --novideo --zoom=0.20"], shell=True)
            r = requests.post('http://' + relay_ip + '/relays.cgi?relay=1')
            print("Started "+rtsp_link+" at "+current_time)

            pid_vlc = proc.pid
            last_slot = active_slot

        if last_slot != active_slot and active_slot is None:
            if sys.platform != 'darwin':
                subprocess.Popen(['powershell.exe', 'Stop-Process -name vlc -Force'], shell=True)
            else:
                subprocess.Popen(['kill -9 ' + str(pid_vlc)], shell=True)
            r = requests.post('http://' + relay_ip + '/relays.cgi?relay=1')
            print("Stopped " + rtsp_link + " at " + current_time)
            last_slot = active_slot
            pid_vlc = None

        time.sleep(60)
