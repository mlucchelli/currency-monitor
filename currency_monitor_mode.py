from graph_drawer_320 import GraphDrawer320
import utime

class CurrencyMonitorMode:
    def __init__(self, display_manager, progress_bar, currencies_data):
        self.display_manager = display_manager
        self.progress_bar = progress_bar
        self.graph_drawer = GraphDrawer320(self.display_manager.display, 320, 170, 10, self.display_manager.white)
        self.currencies_data = currencies_data
        self.history_retention = currencies_data.days
        self.current_currency_index = -1
        self.current_currency = ""
        self.last_action_time = utime.ticks_ms()
        self.interval_minutes = 1

    def draw_screen_original(self, cached = False):
        self.progress_bar.update(10)
        self.progress_bar.draw()

        output_text = self.currencies_data.get_latest_value(self.current_currency, cached)
        self.progress_bar.update(50)
        self.progress_bar.draw()

        values = self.currencies_data.get_history(self.history_retention, self.current_currency, cached)
        self.progress_bar.update(100)
        self.progress_bar.draw()
        self.display_manager.display.clear()
        self.display_manager.display_currency(output_text, 10, 180, self.display_manager.white, None)
        self.graph_drawer.draw_evolution_graph(values, False)

    def draw_screen(self, cached = False):
        self.progress_bar.update(10)
        self.progress_bar.draw()

        output_text = self.currencies_data.get_latest_value(self.current_currency, cached)
        self.progress_bar.update(50)
        self.progress_bar.draw()

        values = self.currencies_data.get_history(self.history_retention, self.current_currency, cached)
        self.progress_bar.update(100)
        self.progress_bar.draw()
        self.display_manager.display.clear()
        self.display_manager.display_currency(output_text, 10, 182, self.display_manager.black, self.display_manager.white)
        self.graph_drawer.draw_evolution_graph(values, False)

    def draw(self):
         elapsed_minutes = (utime.ticks_ms() - self.last_action_time) / 60000
         if elapsed_minutes >= self.interval_minutes:
            self.draw_screen(False)
            self.last_action_time = utime.ticks_ms()

    def update(self, pot_control):
        potentiometer_value = pot_control.read(len(self.currencies_data.currencies_index))

        if(self.current_currency_index != potentiometer_value):
            self.current_currency_index = potentiometer_value
            self.current_currency = self.currencies_data.currencies_index[self.current_currency_index]
            print(self.current_currency)
            print("update screen from cache")
            print(self.currencies_data.currency_color(self.current_currency))
            pot_control.set_rgb_color(self.currencies_data.currency_color(self.current_currency))
            self.draw_screen(True)

    def init(self):
        self.display_manager.display.clear()
        self.display_manager.print_display('Fetching data', 10, 10, 10, 5, 255, "", 255)
        self.currencies_data.load_data(self.progress_bar)
        print(self.currencies_data.currencies_index)
