import pygame
from colors import *

width = 800
height = 800

assets = {}
rendered_objects = []
background = None
screen = None


def update():
    global screen, background, rendered_objects, width, height
    screen.fill(black)

    if background:
        screen.blit(background, (0, 0, width, height))

    for r in rendered_objects:
        r.render(screen)

    pygame.display.flip()


def register(thing):
    global rendered_objects
    if thing not in rendered_objects:
        rendered_objects.append(thing)


def remove(thing):
    global rendered_objects
    if thing in rendered_objects:
        rendered_objects.remove(thing)


def init(w, h, cell_size, menu_width, playfield_w, playfield_h, background_line_width):
    global screen, background, width, height
    pygame.display.init()
    width = w
    height = h
    screen = pygame.display.set_mode((width, height))
    background = pygame.Surface((width, height))
    background.fill(background_color)
    for i in range(playfield_w):
        pygame.draw.line(background, background_line_color, (cell_size * i + menu_width, 0),
                         (cell_size * i + menu_width, height), background_line_width)
    for i in range(playfield_h):
        pygame.draw.line(background, background_line_color, (menu_width, cell_size * i), (width, cell_size * i),
                         background_line_width)


def load(file):
    global assets
    if file in assets:
        return assets[file]
    else:
        image = pygame.image.load(file)
        assets[file] = image
        return image
