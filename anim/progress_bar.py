class ProgressBar:
    def __init__(self, display):
        self.display = display
        self.WIDTH, self.HEIGHT = self.display.get_bounds()
        self.x = 10
        self.y = self.HEIGHT - 5
        self.width = self.WIDTH - 20
        self.height = 10
        self.progress = 0

    def update(self, percentage):
        self.progress = max(0, min(100, percentage))

    def draw(self):
        # Dibuja el borde del área de la barra de progreso
        self.display.rectangle(self.x, self.y, self.width, self.height)

        # Calcula la longitud de la barra de progreso según el porcentaje
        progress_width = (self.width - 2) * (self.progress / 100)

        # Dibuja la barra de progreso
        progress_color = self.display.create_pen(0, 255, 0)
        self.display.set_pen(255)
        self.display.rectangle(int(self.x + 1), int(self.y + 1), int(progress_width), int(self.height - 2))

        self.display.update()
        self.display.set_pen(0)

