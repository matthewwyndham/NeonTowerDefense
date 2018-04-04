import pygame
import enums
from colors import *


# outside the class you must check:
# self.alive -> delete this enemy from the list if it is not alive
# self.hurts -> enemy has reached the end of the paths, so hurt
#               the player and delete this enemy from the list
class Enemy:
    def __init__(self, id, size, etype, level, wave, pos=(0, 0)):
        self.id = id
        self.x = -size + pos[0]
        self.y = 0 + pos[1]
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
        self.color = enemy_colors[self.t][0], 30 * self.t, enemy_colors[self.t][2]
        self.poisoned = False
        self.iced = False

    def pos(self):
        return self.x, self.y

    def center(self):
        return self.x + (self.s // 2), self.y + (self.s // 2)

    def box(self):
        return pygame.Rect((self.x, self.y), (self.s, self.s))

    def speed(self):
        if self.iced:
            return (enums.enemy_speed[self.t] / 3) * 2
        else:
            return enums.enemy_speed[self.t]

    def max_health(self): return self.m_hp

    def current_health(self): return self.hp

    def damage(self, power):
        self.hp -= power
        self.color = (self.color[0], (self.color[1] - self.hp) % 255, self.color[2])
        if self.hp < 1:
            self.alive = False

    def render(self, surf):
        pygame.draw.rect(surf, self.color, self.box())

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
            if self.box().collidepoint(goal[0] + 10, goal[1] + 10):
                self.current_path_spot += 1

            if self.poisoned:
                self.damage(0.1)
        else:
            self.hurts = True
