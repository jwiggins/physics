import sys

from pygame import init, display, event, locals, Color
from pygame.time import Clock

black = Color(0, 0, 0)
white = Color(255, 255, 255)

def load():
    pass


def update(dt):
    pass


def draw(surface):
    surface.fill(black)


if __name__ == '__main__':
    init()
    fps_clock = Clock()
    window_surface = display.set_mode((800, 600))
    display.set_caption("Pygame test")

    while True:
        for evnt in event.get():
            if evnt.type == locals.QUIT:
                sys.exit()

        update(fps_clock.tick(30))

        draw(window_surface)
        display.update()
