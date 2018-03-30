import pygame
import math
from colors import *

class Gun:
    def __init__(self, base, size, style, color, level):
        self.x = base[0]
        self.y = base[1]
        self.aim = (0, 0)
        self.length = size
        self.inner = size / 2
        self.style = style
        self.color = color
        self.level = level

    def render(self, surf):
        pass  # TODO: draw a line

    def update(self, pos):
        self.aim = pos
