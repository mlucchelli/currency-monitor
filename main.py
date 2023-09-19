import utime
import time
import network
import urequests as requests
import machine
from machine import Pin
from display_manager import DisplayManager
from currencies_data import CurrenciesData
from graph_drawer import GraphDrawer

# end of import
led_pin = Pin(15, Pin.OUT)
potentiometer_pin = machine.ADC(machine.Pin(28))
display_manager = DisplayManager(255)
WIDTH, HEIGHT = display_manager.display.get_bounds()
graph_drawer = GraphDrawer(display_manager.display, 150, 10)

currencies_data = CurrenciesData(led_pin)
current_currency_index = 0
current_currency = currencies_data.currencies_index[current_currency_index]

potentiometer_min = 1000
potentiometer_max = 65000
output_min = 0
output_max = 90
desired_values = 100

interval_minutes = 10
last_action_time = utime.ticks_ms() - (interval_minutes * 60000)

ssid = '***REMOVED***'
password = '***REMOVED***'

# end of variable init

led_pin.value(0)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

#
# Main
#
display_manager.print_display('Init', 10, 10, 10, 5, 255, "", 255)

max_wait = 20
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    display_manager.display.clear()
    display_manager.print_display('waiting for connection ({})'.format(max_wait), 10, 10, 10, 4, 255, "", 255)
    display_manager.display.update()
    utime.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('Network Connection has failed')
else:
    print('connected')
    display_manager.display.clear()
    display_manager.print_display('connected!', 10, 10, 10, 5, 255, "", 255)
    display_manager.display.update()

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def update_screen_data(cached = False):
    print(current_currency)
    display_manager.display.clear()
    output_text = currencies_data.get_current_value(current_currency, cached)
    display_manager.print_display(output_text, 10, 180, 230, 5, 255, "", 255)
    values = currencies_data.get_history(90, current_currency, cached)
    graph_drawer.draw_evolution_graph(values)

def update_currency_input():
    global current_currency_index, current_currency
    potentiometer_value = potentiometer_pin.read_u16()
    mapped_value = map_value(potentiometer_value, potentiometer_min, potentiometer_max, output_min, output_max)
    print(mapped_value)
    if(mapped_value > 1):
            mapped_value = 1

    if(current_currency_index != mapped_value):
        current_currency_index = mapped_value
        current_currency = currencies_data.currencies_index[current_currency_index]
        print("update screen from cache")
        update_screen_data(True)
        #utime.sleep(1)

while True:
    try:
        elapsed_minutes = (utime.ticks_ms() - last_action_time) / 60000
        if elapsed_minutes >= interval_minutes:
            update_screen_data(False)
            last_action_time = utime.ticks_ms()
        else:
            update_currency_input()
        

    except Exception as e:
        print("could not connect (status =" + str(wlan.status()) + ")")
        print(e)
        if wlan.status() < 0 or wlan.status() >= 3:
            print("trying to reconnect...")
            wlan.disconnect()
            wlan.connect(ssid, password)
            if wlan.status() == 3:
                print('connected')
            else:
                print('connection failed: ' + e)
    display_manager.display.update()
    #utime.sleep(1) 


#current_time = time.localtime()
#current_date = "{:04d}-{:02d}-{:02d}".format(current_time[0], current_time[1], current_time[2])

#print("time")
#print(current_date)




