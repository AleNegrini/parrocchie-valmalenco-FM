import time
import sys
import subprocess
import requests
from parrocchie_valmalenco_fm.utils import get_current_date, get_current_time, active_slot
from parrocchie_valmalenco_fm.reader import read_file
from parrocchie_valmalenco_fm.config import Config
from parrocchie_valmalenco_fm.camera_config import CameraConfig

ORARI_FILE = 'orari.csv'
RELAY_CONFIG_FILE = 'config-relay.ini'
CMAERA_CONFIG_FILE = 'config.ini'

if __name__ == '__main__':

    # validate the presence of required config files
    config = Config()
    config_path_dict = config.config_check([ORARI_FILE, RELAY_CONFIG_FILE, CMAERA_CONFIG_FILE])
    cameras = CameraConfig(config_path_dict[CMAERA_CONFIG_FILE])
    relay_ip = config.get_relay_ip(config_path_dict[RELAY_CONFIG_FILE])

    last_slot = None
    pid_vlc = None
    while True:
        current_date = get_current_date()
        current_time = get_current_time()
        calendar = read_file(config_path_dict[ORARI_FILE])

        if last_slot != active_slot(current_date, current_time, calendar) and \
                active_slot(current_date, current_time, calendar) is not None:

            # build the rtsp link
            rtsp_link = "rtsp://" + \
                  cameras.user_dict[active_slot(current_date, current_time, calendar)] + ":" + \
                  cameras.pass_dict[active_slot(current_date, current_time, calendar)] + "@" + \
                  cameras.ip_dict[active_slot(current_date, current_time, calendar)] + \
                  ":" + \
                  cameras.port_dict[active_slot(current_date, current_time, calendar)]
                  # "/Streaming/Channels/"+ \
                  # Constants.channel_dict[active_slot(current_date, current_time, calendar)]

            if sys.platform != 'darwin':
                proc = subprocess.Popen(['powershell.exe',
                                         "C:/'Program Files'/VideoLAN/VLC/vlc.exe " + rtsp_link +
                                         " --novideo --zoom=0.20"],
                                        stdout=sys.stdout)
            else:
                proc = subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC ' + rtsp_link +
                                         " --novideo --zoom=0.20"],
                                        shell=True)
            r = requests.post('http://' + relay_ip + '/relays.cgi?relay=1')
            print("Started "+rtsp_link+" at "+current_time)
            pid_vlc = proc.pid

            last_slot = active_slot(current_date, current_time, calendar)

        if last_slot != active_slot(current_date, current_time, calendar) and \
                active_slot(current_date, current_time, calendar) is None:
            if sys.platform != 'darwin':
                subprocess.Popen(['powershell.exe',
                                  'Stop-Process -name vlc -Force'],
                                  shell=True)
            else:
                subprocess.Popen(['kill -9 '+str(pid_vlc)], shell=True)
            r = requests.post('http://' + relay_ip + '/relays.cgi?relay=1')
            print("Stopped " + rtsp_link+" at "+current_time)
            last_slot = active_slot(current_date, current_time, calendar)
            pid_vlc = None

        time.sleep(60)



