class GraphDrawer:
    def __init__(self, display, height, offset):
        self.display = display
        self.height = height
        self.offset = offset

    def draw_evolution_graph(self, values):
        self.display.set_pen(255)
        
        WIDTH, _ = self.display.get_bounds()
        y_min = min(values)
        y_max = max(values)
        num_points = len(values)

        if num_points <= 1:
            return
   
        scale_y = (self.height - self.offset) / (y_max - y_min)
        spacing_between_points = WIDTH // (num_points - 1)

        self.display.line(0, self.height + self.offset, WIDTH, self.height + self.offset)
        self.display.line(0, self.offset, 0, self.height + self.offset)

        prev_x, prev_y = None, None
        for i, value in enumerate(values):
            x = i * spacing_between_points
            y = self.height - self.offset - int((value - y_min) * scale_y)

            self.display.line(x, self.height + self.offset, x, self.height + self.offset - 5)

            if prev_x is not None:
                self.display.line(prev_x, prev_y, x, y)

            prev_x, prev_y = x, y
        self.display.set_pen(0)
