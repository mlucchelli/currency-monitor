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
        "current": "",
        "historic": "",
    }

    currencies_index = ["dolar_blue", "dolar_oficial"]

    def __init__(self, led_pin):
        self.led_pin = led_pin


    def get_current_value(self, currency, cached = False):
        prices = ""
        if(not cached or self.cache["current"] == ""):
            self.led_pin.value(1)
            #data = requests.get("https://api.bluelytics.com.ar/v2/latest")
            data = requests.get("https://api.npoint.io/3ac4dc2da6f4c1218f64")
            prices = data.json()
            self.led_pin.value(0)
            self.cache["current"] = prices
            data.close()
            print("read current from network")
        else:
            prices = self.cache["current"]
            print("read current from cache")
        value = str(prices[currency]['value_buy'])
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
            #data = requests.get("https://api.bluelytics.com.ar/v2/evolution.json?days={}".format(days))
            data = requests.get("https://api.npoint.io/cd424be197aed8ba4eb4")
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

