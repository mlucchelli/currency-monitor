from picographics import PicoGraphics, DISPLAY_LCD_240X240, PEN_P8, PEN_RGB332
import jpegdec

class DisplayManager:
    def __init__(self, pen_color):
        self.display = PicoGraphics(display=DISPLAY_LCD_240X240, pen_type=PEN_RGB332)
        self.display.set_backlight(0.9)
        self.display.set_font("bitmap8")
        self.jpeg_decoder = jpegdec.JPEG(self.display)
        self.pen_color = pen_color
        self.max_lines = 10
        self.lines = []

    def print_image(self, filename):
        self.jpeg_decoder.open_file(filename)
        self.jpeg_decoder.decode(2, 110, jpegdec.JPEG_SCALE_FULL, dither=False)

    def print_display(self, output_text, x, y, wordwrap, scale, font_color, font, bg_color):
        self.display.set_pen(font_color)
        self.display.text(output_text, x, y, wordwrap, scale)
        self.display.set_pen(0)

    def set_pen(self, color):
       self.display.set_pen(color)

    def log(self, text):
        self.lines.append(text)

        if len(self.lines) > self.max_lines:
            self.lines.pop(0)

        self.display.clear()

        y = 0
        for line in self.lines:
            self.display.text(str(line), 0, y, scale=2)
            y += 16

        self.display.update()