import urequests as requests
from machine import Pin

class CurrenciesData:
    currencies = {
        "dolar_blue":{
            "name": "USDb",
        },
         "dolar_oficial":{
            "name": "USD"
        }
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

    currencies_index = ["dolar_blue", "dolar_oficial"]

    def __init__(self, led_pin, env = "prod"):
        self.led_pin = led_pin
        self.env = env
        self.host_url = self.env_vars[env]["host_url"]


    def get_latest_value(self, currency, cached = False):
        prices = ""
        if(not cached or self.cache["latest"] == ""):
            self.led_pin.value(1)
            print("url "+ self.host_url + "/latest")
            data = requests.get(self.host_url + "/latest")
            prices = data.json()
           
            self.led_pin.value(0)
            self.cache["latest"] = prices
            data.close()
            print("read latest from network")
        else:
            prices = self.cache["latest"]
            print("read latest from cache")
        value = str(int(float(prices[currency]['value_avg'])))
        output_text = self.currencies[currency]["name"] + " $" + value
        
        return output_text

    def get_historic_value_buy(self, data, currency):
        values_for_currency = data[currency]
        values_for_currency.sort(key=lambda x: x["date"])
        buy_values = [int(item["value_buy"]) for item in values_for_currency]
        return buy_values

    def get_history(self, days, currency, cached = False):
        all_historic_values = ""
        if(not cached or self.cache["historic"] == ""):
            self.led_pin.value(1)
            print("url "+ self.host_url + "/historic?days={}".format(days))
            data = requests.get(self.host_url + "/historic?days={}".format(days))
            all_historic_values = data.json()
            data.close()
            self.cache["historic"] = all_historic_values
            self.led_pin.value(0)
            print("read historic from network")
        else:
            all_historic_values = self.cache["historic"]
            print("read historic from cache")

        values = self.get_historic_value_buy(all_historic_values, currency)
        return values

