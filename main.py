import utime
import time
import network
import urequests as requests
import machine
from machine import Pin
from display_manager import DisplayManager
from currencies_data import CurrenciesData
from graph_drawer import GraphDrawer
from network_manager import NetworkManager
from anim.tv_animation import TVAnimation
from anim.progress_bar import ProgressBar

# end of import
env = "prod"
potentiometer_min = 1000
potentiometer_max = 65000
output_min = 0
output_max = 90
desired_values = 100

interval_minutes = 10
last_action_time = utime.ticks_ms() - (interval_minutes * 60000)

ssid = '***REMOVED***'
password = '***REMOVED***'
led_pin = Pin(15, Pin.OUT)
potentiometer_pin = machine.ADC(machine.Pin(28))
display_manager = DisplayManager(255)

tv_animation = TVAnimation(display_manager.display)
tv_animation.run_animation()

#particles_animation = ParticlesAnimation(display_manager.display)
#particles_animation.run_animation()

progress_bar = ProgressBar(display_manager.display)

graph_drawer = GraphDrawer(display_manager.display, 170, 10)

currencies_data = CurrenciesData(led_pin, env)

current_currency_index = 0
current_currency = currencies_data.currencies_index[current_currency_index]

network_manager = NetworkManager(ssid,password, display_manager)

# end of variable init

#
# Main
#
display_manager.print_display('Init', 10, 10, 10, 5, 255, "", 255)
led_pin.value(0)
network_manager.connect_wifi()

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def update_screen_data(cached = False):
    progress_bar.update(10)
    progress_bar.draw()

    output_text = currencies_data.get_latest_value(current_currency, cached)
    progress_bar.update(90)
    progress_bar.draw()
    
    values = currencies_data.get_history(90, current_currency, cached)
    display_manager.display.clear()
    display_manager.print_display(output_text, 10, 195, 230, 4, 255, "", 255)
    graph_drawer.draw_evolution_graph(values)
    progress_bar.update(0)
    progress_bar.draw()

def update_currency_input():
    global current_currency_index, current_currency
    potentiometer_value = potentiometer_pin.read_u16()
    mapped_value = map_value(potentiometer_value, potentiometer_min, potentiometer_max, output_min, output_max)
   
    if(mapped_value > 1):
            mapped_value = 1

    if(current_currency_index != mapped_value):
        current_currency_index = mapped_value
        current_currency = currencies_data.currencies_index[current_currency_index]
        print(current_currency)
        print("update screen from cache")
        update_screen_data(True)
        #utime.sleep(1)

display_manager.display.clear()
display_manager.print_display('Fetching data', 10, 10, 10, 5, 255, "", 255)
display_manager.display.update()

while True:
    try:
        elapsed_minutes = (utime.ticks_ms() - last_action_time) / 60000
        if elapsed_minutes >= interval_minutes:
            update_screen_data(False)
            last_action_time = utime.ticks_ms()
        else:
            update_currency_input()
        

    except Exception as e:
        print(e)
        print("could not connect (status =" + str(network_manager.wlan.status()) + ")")
        if network_manager.wlan.status() < 0 or network_manager.wlan.status() >= 3:
            print("trying to reconnect...")
            network_manager.connect_wifi()
            if network_manager.wlan.status() == 3:
                print('connected')
            else:
                print('connection failed: ' + e)
    display_manager.display.update()
    #utime.sleep(1) 


#current_time = time.localtime()
#current_date = "{:04d}-{:02d}-{:02d}".format(current_time[0], current_time[1], current_time[2])

#print("time")
#print(current_date)




