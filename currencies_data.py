import gc
import time
import urllib.urequest as requests
import ujson
from machine import Pin

class CurrenciesData:

    cache = {
        "latest": "",
        "historic": "",
    }

    env_vars = {
        "local":{
            "host_url": "http://localhost:3000",
        },
         "prod":{
            "host_url": "https://currency-monitor-api-eu.onrender.com"
        }
    }

    def __init__(self, led_pin, days, env = "prod"):
        self.led_pin = led_pin
        self.env = env
        self.days = days
        self.host_url = self.env_vars[env]["host_url"]
        self.currencies_index = []


    def get_latest_values(self):
        self.led_pin.on()
        data = bytearray(2048)
        print("url " + self.host_url + "/latest")
        r = requests.urlopen(self.host_url + "/latest")
        r.readinto(data)
        self.cache["latest"] = ujson.loads(data)
        
        r.close()
        del r
        del data
        print("read latest from network")
        # new request could include new currencies
        self.currencies_index = []
        for currency in self.cache["latest"]:
            self.currencies_index.append(currency)

        self.led_pin.off()
        return self.cache["latest"]
    
    def get_latest_value(self, currency, cached = False):
        prices = ""
        if(not cached or self.cache["latest"] == ""):
            prices = self.get_latest_values()
        else:
            prices = self.cache["latest"]
            print("read latest from cache")
        value = float(prices[currency]['value_avg'])
        if(value > 99):
            value = int(value)

        output_text = currency + " $" + str(value)
        del prices
        gc.collect()
        return output_text

    def get_historic_value_buy(self, data, currency):
        values_for_currency = data[currency]
        #values_for_currency.sort(key=lambda x: x["date"])
        buy_values = [float(item["value_buy"]) for item in values_for_currency]
        return buy_values

    def get_all_history(self, days):
        self.led_pin.on()
        data = bytearray(13000)
        print("url "+ self.host_url + "/historic/{}".format(days))
        r = requests.urlopen(self.host_url + "/historic/{}".format(days))
        r.readinto(data)
        self.cache["historic"] = ujson.loads(data)
        #values = self.get_historic_value_buy(all_historic_values, currency)
        r.close()
        del r
        del data

        self.led_pin.off()
        print("read historic from network")
        return self.cache["historic"] 

    def get_history(self, days, currency, cached = False):
        all_historic_values = ""
        values = ""
        if(not cached or self.cache["historic"] == ""):
            all_historic_values = self.get_all_history(days)
        else:
            all_historic_values = self.cache["historic"]
            #values = self.get_historic_value_buy(all_historic_values, currency)
            print("read historic from cache")
        values = self.get_historic_value_buy(all_historic_values, currency)
        del all_historic_values
        gc.collect()
        return values
    
    def currency_color(self, currency):
        color_parts = self.cache["latest"][currency]["color"].split(",")
        return {
            "r": int(color_parts[0]),
            "g": int(color_parts[1]),
            "b": int(color_parts[2])
        }       


    def load_data(self, progress_bar = None):
        progress_bar.update(10)
        progress_bar.draw()

        self.get_latest_values()
        gc.collect()
        progress_bar.update(50)
        progress_bar.draw()
        
        self.get_all_history(self.days)
        gc.collect()
        progress_bar.update(100)
        progress_bar.draw()
