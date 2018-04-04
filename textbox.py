import pygame
from colors import *


class Textbox:
    def __init__(self, pos, color, font, text, floating=False):
        self.pos = pos
        self.color = color
        self.font = font
        self.text = text
        self.floating_textbox = floating

        self.identity = -2  # -2 is a textbox

    def render(self, surf):
        text = self.font.render(self.text, False, self.color)
        if self.floating_textbox:
            text = self.font.render(self.text, False, self.color, black)
        surf.blit(text, self.pos)

