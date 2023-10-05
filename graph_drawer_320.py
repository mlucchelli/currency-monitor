from drivers.ili9341 import color565

class GraphDrawer320:
    def __init__(self, display, width, height, offset, color):
        self.display = display
        self.width = width
        self.height = height
        self.offset = offset
        self.color = color
        self.red = color565(255, 0, 0)
        self.green = color565(0, 255, 0)

    def draw_evolution_graph(self, values, show_fluctuation=False):
        y_min = min(values)
        y_max = max(values)
        num_points = len(values)

        if num_points <= 1:
            return

        scale_y = (self.height - self.offset) / (y_max - y_min)
        spacing_between_points = self.width // (num_points - 1)

        # Grosor de los ejes
        axis_thickness = 3

        # Dibuja ejes más gruesos
        self.display.fill_rectangle(0, self.height - axis_thickness, self.width, axis_thickness, self.color)  # Eje X
        self.display.fill_rectangle(0, 0, axis_thickness, self.height, self.color)  # Eje Y

        prev_x, prev_y = None, None
        for i, value in enumerate(values):
            x = i * spacing_between_points
            y = self.height - self.offset - int((value - y_min) * scale_y)

            if prev_x is not None:

                if show_fluctuation:
                    prev_value = values[i - 1]
                    rect_color = self.red if value < prev_value else self.green
                    rect_width = 4
                    rect_height = 8
                    rect_x = x - rect_width 
                    rect_y = y - rect_height 
                    self.display.fill_rectangle(rect_x, rect_y, rect_width, rect_height, rect_color)

                self.display.draw_line(prev_x, prev_y, x, y, self.color)

            prev_x, prev_y = x, y
