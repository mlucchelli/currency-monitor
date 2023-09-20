import gc
import time
import urllib.urequest as requests
import ujson
from machine import Pin

class CurrenciesData:
    currencies = {
        "dolar_blue":{
            "name": "USDb",
        },
         "dolar_oficial":{
            "name": "USD"
        },
        "EUR":{
            "name": "EUR"
        },
        "GBP":{
            "name": "GBP"
        },
        "JPY":{
            "name": "JPY"
        },
        "BTC":{
            "name": "BTC"
        },
        "ETH":{
            "name": "ETH"
        },
    }

    cache = {
        "latest": "",
        "historic": "",
    }

    env_vars = {
        "local":{
            "host_url": "http://localhost:3000",
        },
         "prod":{
            "host_url": "https://currency-monitor-api.onrender.com"
        }
    }

    currencies_index = ["dolar_blue", "dolar_oficial", "EUR", "GBP", "JPY", "BTC", "ETH"]

    def __init__(self, led_pin, env = "prod"):
        self.led_pin = led_pin
        self.env = env
        self.host_url = self.env_vars[env]["host_url"]


    def get_latest_value(self, currency, cached = False):
        prices = ""
        if(not cached or self.cache["latest"] == ""):
            self.led_pin.value(1)
            data = bytearray(2048)
            print("url " + self.host_url + "/latest")
            r = requests.urlopen(self.host_url + "/latest")
            r.readinto(data)
            prices = ujson.loads(data)
            #print(jsonData)
            r.close()
            del r
            del data
            self.cache["latest"] = prices
            print("read latest from network")
            self.led_pin.value(0)
        else:
            prices = self.cache["latest"]
            print("read latest from cache")
        value = float(prices[currency]['value_avg'])
        if(value > 9999):
            value = int(value)

        output_text = self.currencies[currency]["name"] + " $" + str(value)
        del prices
        gc.collect()
        return output_text

    def get_historic_value_buy(self, data, currency):
        values_for_currency = data[currency]
        values_for_currency.sort(key=lambda x: x["date"])
        buy_values = [float(item["value_buy"]) for item in values_for_currency]
        return buy_values

    def get_history(self, days, currency, cached = False):
        all_historic_values = ""
        values = ""
        if(not cached or self.cache["historic"] == ""):
            self.led_pin.value(1)
            data = bytearray(13000)
            print("url "+ self.host_url + "/historic/{}".format(days))
            r = requests.urlopen(self.host_url + "/historic/{}".format(days))
            r.readinto(data)
            all_historic_values = ujson.loads(data)
            #values = self.get_historic_value_buy(all_historic_values, currency)
            r.close()
            del r
            del data
            self.cache["historic"] = all_historic_values
            self.led_pin.value(0)
            print("read historic from network")
        else:
            all_historic_values = self.cache["historic"]
            #values = self.get_historic_value_buy(all_historic_values, currency)
            print("read historic from cache")
        values = self.get_historic_value_buy(all_historic_values, currency)
        del all_historic_values
        gc.collect()
        return values

