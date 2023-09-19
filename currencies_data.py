import urequests as requests
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
        value = float(prices[currency]['value_avg'])
        if(value > 9999):
            value = int(value)

        output_text = self.currencies[currency]["name"] + " $" + str(value)
        
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
            print("url "+ self.host_url + "/historic/{}".format(days))
            data = requests.get(self.host_url + "/historic/{}".format(days))
            all_historic_values = data.json()
            #values = self.get_historic_value_buy(all_historic_values, currency)
            data.close()
            self.cache["historic"] = all_historic_values
            self.led_pin.value(0)
            print("read historic from network")
        else:
            all_historic_values = self.cache["historic"]
            #values = self.get_historic_value_buy(all_historic_values, currency)
            print("read historic from cache")

        values = self.get_historic_value_buy(all_historic_values, currency)
        return values

