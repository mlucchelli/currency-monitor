# network_manager.py

import network
import utime
from display_manager import DisplayManager

class NetworkManager:
    def __init__(self, ssid, password, display_manager):
        self.ssid = ssid
        self.password = password
        self.display_manager = display_manager

    def connect_wifi(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.ssid, self.password)

        max_wait = 20
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print('Waiting for connection...')
            self.display_manager.display.clear()
            self.display_manager.print_display('Waiting for connection ({})'.format(max_wait), 10, 10, 10, 4, 255, "", 255)
            self.display_manager.display.update()
            utime.sleep(1)

        if wlan.status() != 3:
            raise RuntimeError('Network Connection has failed')
        else:
            print('Connected')
            self.display_manager.display.clear()
            self.display_manager.print_display('Connected!', 10, 10, 10, 5, 255, "", 255)
            self.display_manager.display.update()
