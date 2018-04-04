import pygame
from colors import *


class Box:
    def __init__(self, pos, size, color=white):
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.color = color
        self.identity = -3  # generic renderable

    def render(self, surf):
        pygame.draw.rect(surf, self.color, pygame.Rect(self.x, self.y, self.width, self.height), 3)