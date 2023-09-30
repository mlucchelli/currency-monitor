from ili9341 import Display, color565
from machine import Pin, SPI
from xglcd_font import XglcdFont

class DisplayManager320:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 320, 240
        spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(15))
        self.display = Display(spi, dc=Pin(11), cs=Pin(13), rst=Pin(12), width=320, height=240, rotation=90)
        self.black = color565(0, 0, 0)
        self.gray3 = color565(78, 78, 78)
        self.gray2 = color565(83, 83, 83)
        self.gray1 = color565(88, 88, 88)
        self.white = color565(255, 255, 255)
        self.red = color565(255, 0, 0)
        self.green = color565(0, 255, 0)
        self.amber = color565(255, 194, 0)
        self.orange = color565(255, 87, 51)
        self.font_unispace_12x24 = XglcdFont('fonts/Unispace12x24.c', 12, 24)
       
    
    def load_fonts(self):
        #self.font_scpro_31x55= XglcdFont('fonts/SCProSB31x55.h', 31, 55)
        #self.arial_32x34 = XglcdFont('fonts/ArialR32x34.h', 32, 34)
        self.neu_42x35 = XglcdFont('fonts/Neu42x35.h', 42, 35)
        #self.times_39x37 = XglcdFont('fonts/TimesNR39x37.h', 39, 37)
        #self.unispace_12x24 = XglcdFont('fonts/Unispace12x24.c', 12, 24)
        #self.font_scpro_31x55 = XglcdFont('fonts/SCProSB31x55.h', 31, 55)
    
    def print_display(self, output_text, x, y, wordwrap, scale, font_color, font, bg_color):
        self.display.draw_text(x, y, output_text, self.font_unispace_12x24, self.white)
    
    def display_currency(self, output_text, x, y, font_color, bg_color):
        background = 0
        if bg_color is not None:
            rect_x = 5  
            rect_y = self.display.height - 60
            rect_width = self.display.width - 10
            rect_height = 40
            self.display.fill_rectangle(rect_x, rect_y, rect_width, rect_height, bg_color)
            self.display.draw_rectangle(rect_x, rect_y, rect_width, rect_height, bg_color)
            background = bg_color

        self.display.draw_text(x, y, output_text, self.neu_42x35, font_color, background=background)

    def clear(self):
         self.display.fill_rectangle(0, 0, self.WIDTH, self.HEIGHT, self.black)


def display_currency2(self, output_text, x, y, font_color, bg_color):
        background = 0
        if bg_color is not None:
            rect_x = 5  
            rect_y = self.display.height - 30
            rect_width = self.display.width - 10
            rect_height = 30
            self.display.fill_rectangle(rect_x, rect_y, rect_width, rect_height, bg_color)
            self.display.draw_rectangle(rect_x, rect_y, rect_width, rect_height, bg_color)
            background = bg_color

        self.display.draw_text(x, y, output_text, self.neu_42x35, font_color, background=background)
