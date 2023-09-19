import utime
import random
from picographics import PicoGraphics, DISPLAY_LCD_240X240, PEN_RGB332, rgb

class ParticlesAnimation:
    def __init__(self, display):
        self.display = display
        self.WIDTH, self.HEIGHT = display.get_bounds()

    def run_animation(self):
        # Colores de las partículas (multicolor)
        particle_colors = [
            rgb(255, 0, 0),   # Rojo
            rgb(0, 255, 0),   # Verde
            rgb(0, 0, 255),   # Azul
            rgb(255, 255, 0), # Amarillo
        ]

        # Tiempo de espera entre fotogramas (en segundos)
        frame_delay = 0.01  # Hacer la animación más fluida

        # Lista de partículas (coordenadas x, y, color)
        particles = []

        while True:
            # Generar una nueva partícula en la parte superior de la pantalla
            color = random.choice(particle_colors)
            x = random.randint(0, self.WIDTH - 1)
            y = 0
            particles.append((x, y, color))

            self.display.clear()

            # Dibujar todas las partículas
            for particle in particles:
                x, y, color = particle
                self.display.set_pen(color)
                self.display.pixel(x, y)
                particle[1] += 1  # Mover la partícula hacia abajo

            self.display.update()

            # Eliminar las partículas que han salido de la pantalla
            particles = [particle for particle in particles if particle[1] < self.HEIGHT]

            # Espera un poco antes de continuar
            utime.sleep(frame_delay)