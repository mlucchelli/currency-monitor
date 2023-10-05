from drivers.ili9341 import color565
class TVAnimation320:
    def __init__(self, display):
        self.display = display
        self.WIDTH = display.width
        self.HEIGHT = display.height

        self.black = color565(0, 0, 0)
        self.white = color565(255, 255, 255)

        self.animation_duration = 5
        self.frame_delay = 0.0

        self.x = self.WIDTH // 2
        self.y = self.HEIGHT // 2

        self.line_length = 0
        self.line_thickness = 4
        self.line_direction = -1

    def draw_pixel(self, x, y, color):
        self.display.draw_pixel(x, y, color)

    def tv_power_on_animation(self):
        while self.line_length <= self.WIDTH // 2:
            self.draw_pixel(self.x, self.y, self.white)
            self.display.fill_rectangle(
                self.x - self.line_length,
                self.y - self.line_thickness // 2,
                2 * self.line_length,
                self.line_thickness,
                self.white,
            )
            self.line_length += 1
            #time.sleep(self.frame_delay)

    def run_animation(self):
        self.tv_power_on_animation()
