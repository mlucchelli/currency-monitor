# network_manager.py

import network
import utime

class NetworkManager:
    def __init__(self, ssid, password, display_manager, led_pin):
        self.ssid = ssid
        self.password = password
        self.display_manager = display_manager
        self.led_pin = led_pin

    def connect_wifi(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.ssid, self.password)

        max_wait = 60
        while max_wait > 0:
            self.led_pin.on()
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print('Connecting')
            self.display_manager.display.clear()
            self.display_manager.print_display('Connecting ({})'.format(max_wait), 10, 10, 10, 4, 255, "", 255)
            utime.sleep(0.1)
            self.led_pin.off()

        self.led_pin.off()

        if wlan.status() != 3:
            raise RuntimeError('Network Connection has failed')
        else:
            print('Connected')
            self.display_manager.display.clear()
            self.display_manager.print_display('Connected!', 10, 10, 10, 5, 255, "", 255)

    def connection_enabled(self):
        return self.wlan.status() < 0 or self.wlan.status() >= 3
    
    
