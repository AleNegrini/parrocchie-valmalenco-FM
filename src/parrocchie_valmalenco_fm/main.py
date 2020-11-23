from constants import Constants
import time
import sys
import subprocess
from utils import get_current_date, get_current_time, active_slot
from reader import read_file

if __name__ == '__main__':

    last_slot = None
    pid_vlc = None
    while True:
        current_date = get_current_date()
        current_time = get_current_time()
        calendar = read_file('../resources/orari.csv')

        if last_slot != active_slot(current_date, current_time, calendar) and \
                active_slot(current_date, current_time, calendar) is not None:

            #build the rtsp link
            rtsp_link = "rtsp://"+ \
                  Constants.user_dict[active_slot(current_date, current_time, calendar)] + ":" + \
                  Constants.pass_dict[active_slot(current_date, current_time, calendar)] + "@" + \
                  Constants.ip_dict[active_slot(current_date, current_time, calendar)]+ \
                  ":"+ \
                  Constants.port_dict[active_slot(current_date, current_time, calendar)] + \
                  "/Streaming/Channels/"+ \
                  Constants.channel_dict[active_slot(current_date, current_time, calendar)]

            if sys.platform != 'darwin':
                proc = subprocess.Popen(['powershell.exe',
                                         'C:\\Program Files\VideoLAN\VLC\vlc.exe' + rtsp_link],
                                        stdout=sys.stdout)
            else:
                proc = subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC ' + rtsp_link], shell=True)

            print("Started "+rtsp_link+" at "+current_time)
            pid_vlc = proc.pid

            last_slot = active_slot(current_date, current_time, calendar)

        if last_slot != active_slot(current_date, current_time, calendar) and \
                active_slot(current_date, current_time, calendar) is None:
            if sys.platform != 'darwin':
                subprocess.Popen(['Stop-Process -ID ' + str(pid_vlc) + ' -Force'], shell=True)
            else:
                subprocess.Popen(['kill -9 '+str(pid_vlc)], shell=True)
            print("Stopped " + rtsp_link+" at "+current_time)
            last_slot = active_slot(current_date, current_time, calendar)
            pid_vlc = None

        time.sleep(60)