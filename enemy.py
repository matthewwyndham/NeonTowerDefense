import pygame
import enums
from colors import *


# outside the class you must check:
# self.alive -> delete this enemy from the list if it is not alive
# self.hurts -> enemy has reached the end of the paths, so hurt
#               the player and delete this enemy from the list
class Enemy:
    def __init__(self, id, size, etype, level, wave):
        self.id = id
        self.x = -size
        self.y = 0
        self.s = size
        self.t = etype
        self.level = level
        self.wave = wave
        imported_hp = enums.enemy_health[etype]
        modded_hp = level * imported_hp + (wave * 2)
        self.hp = modded_hp
        self.m_hp = modded_hp
        self.alive = True
        self.current_path_spot = 0
        self.hurts = False

    def pos(self):
        return self.x, self.y

    def center(self):
        return self.x + (self.s // 2), self.y + (self.s // 2)

    def box(self):
        return pygame.Rect((self.x, self.y), (self.s, self.s))

    def speed(self): return enums.enemy_speed[self.t]

    def max_health(self): return self.m_hp

    def current_health(self): return self.hp

    def damage(self, power):
        self.hp -= power
        if self.hp < 1:
            self.alive = False

    def render(self, surf):
        pygame.draw.rect(surf, enemy_colors[self.t], self.box())

    def update(self, path):
        if self.current_path_spot < len(path):
            goal = path[self.current_path_spot]
            if self.x < goal[0]:
                self.x += self.speed()
            if self.x > goal[0]:
                self.x -= self.speed()
            if self.y < goal[1]:
                self.y += self.speed()
            if self.y > goal[1]:
                self.y -= self.speed()
            if self.x == goal[0] and self.y == goal[1]:
                self.current_path_spot += 1
        else:
            self.hurts = True
