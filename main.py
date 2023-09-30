import utime
import machine
from machine import Pin
from display_manager_320 import DisplayManager320
from currencies_data import CurrenciesData
from network_manager import NetworkManager
from anim.tv_animation import TVAnimation
from anim.tv_animation_320 import TVAnimation320
from anim.progress_bar import ProgressBar
from anim.progress_bar_320 import ProgressBar320
from potentiometer_controller import PotentiometerController
from currency_monitor_mode import CurrencyMonitorMode
import gc

# end of import
env = "prod"
history_retention = 30
potentiometer_min = 1500
potentiometer_max = 63000
output_min = 0
output_max = 90
desired_values = 900
ssid = '***REMOVED***'
password = '***REMOVED***'
led_pin = Pin(16, Pin.OUT)
potentiometer_pin = machine.ADC(machine.Pin(28))
beta = True
display_manager = None
tv_animation = None
progress_bar = None
display_manager = DisplayManager320()
tv_animation = TVAnimation320(display_manager.display)
tv_animation.run_animation()
display_manager.load_fonts()
display_manager.clear()
display_manager.print_display('Init', 10, 10, 10, 5, 255, "", 255)
progress_bar = ProgressBar320(display_manager.display, display_manager.white)
network_manager = NetworkManager(ssid,password, display_manager)
currencies_data = CurrenciesData(led_pin, history_retention, env)
PINS_BREAKOUT_GARDEN = {"sda": 18, "scl": 19}
pot_control = PotentiometerController(PINS_BREAKOUT_GARDEN)
currency_monitor_mode = CurrencyMonitorMode(display_manager, progress_bar, currencies_data)
# end of variable init

def draw():
    currency_monitor_mode.draw()
 
def update():
    currency_monitor_mode.update(pot_control)
    

def init():
    led_pin.value(0)
    network_manager.connect_wifi()
    utime.sleep(0.1)
    currency_monitor_mode.init()

#
# Main
#
def main():
    while True:
        # update()
        # draw()
        try:
            update()
            draw()
            # free_memory = gc.mem_free()
            # print("Free memmory:", free_memory, "bytes")
        except Exception as e:
            print(e)
            print("Error: {}".format(e))
            if network_manager.connection_enabled is not True:
                print("trying to reconnect...")
                network_manager.connect_wifi()
                if network_manager.wlan.status() == 3:
                    print('connected')
                else:
                    print('connection failed: ' + e)

init()
main()     
