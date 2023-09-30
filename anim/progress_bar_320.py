class ProgressBar320:
    def __init__(self, display, color):
        self.display = display
        self.WIDTH = display.width
        self.HEIGHT = display.height
        self.x = 10
        self.y = self.HEIGHT - 15
        self.width = self.WIDTH - 20
        self.height = 10
        self.progress = 0
        self.color = color

    def update(self, percentage):
        self.progress = max(0, min(100, percentage))
    
    def draw(self):
        progress_width = (self.width - 2) * (self.progress / 100)
        self.display.fill_rectangle(int(self.x + 1), int(self.y + 1), int(progress_width), int(self.height - 2), self.color)
