import utime

class TVAnimation:
    def __init__(self, display):
        self.display = display
        self.WIDTH, self.HEIGHT = display.get_bounds()

        self.point_color = display.create_pen(255, 255, 255)  # Blanco
        self.line_width = 4  # Ancho de línea en píxeles

        self.x, self.y = self.WIDTH // 2, self.HEIGHT // 2
        self.line_length = 0
        self.line_speed = 8
        self.frame_delay = 0.01

    def run_animation(self):
        while True:
            self.display.set_pen(self.point_color)
            self.display.pixel(self.x, self.y)

            x1, x2 = self.x - self.line_length, self.x + self.line_length
            self.display.set_pen(self.point_color)

            for i in range(-self.line_width // 2, self.line_width // 2 + 1):
                self.display.line(x1, self.y + i, x2, self.y + i)

            self.display.update()

            self.line_length += self.line_speed

            utime.sleep(self.frame_delay)

            if x1 < 0 or x2 >= self.WIDTH:
                break

        self.display.set_pen(self.display.create_pen(0, 0, 0))
        self.display.clear()
        self.display.update()
