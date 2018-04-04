import pygame
from enums import Terrain
from colors import *


class Cell:
    def __init__(self, i, x, y, s, t=Terrain.EMPTY):
        self.identity = i
        self.x = x
        self.y = y
        self.size = s
        self.t = t  # terrain type
        self.box = pygame.Rect((self.x, self.y), (self.size, self.size))

        self.play_lines = [(self.x + (1/4) * self.size, self.y + (1/4) * self.size),
                           (self.x + (3/4) * self.size, self.y + (1/2) * self.size),
                           (self.x + (1/4) * self.size, self.y + (3/4) * self.size)]

    def render(self, surf):
        pygame.draw.rect(surf, terrain_colors[self.t.value], self.box)
        pygame.draw.rect(surf, background_line_color, self.box, 1)
        if self.t.value == Terrain.PLAYBUTTON.value:
            pygame.draw.lines(surf, dark(white), True, self.play_lines, 2)
            pygame.draw.rect(surf, dark(white), self.box, 1)

    def is_in(self, pos):
        if self.x < pos[0] < self.x + self.size:
            if self.y < pos[1] < self.y + self.size:
                return True
        return False

    def pos(self): return self.x, self.y
