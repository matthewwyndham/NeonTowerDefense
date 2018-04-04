import pygame
import enums
from calculations import *
from gun import Gun
from shot import Shot
from colors import *


class Tower:
    def __init__(self, i, x, y, s, t=0):
        self.identity = i
        self.x = x
        self.y = y
        self.size = s
        self.t_num = t
        self.box = pygame.Rect((self.x, self.y), (self.size, self.size))
        self.level = 1
        self.__c_mod = 1.0  # gets smaller
        self.coolness = 0   # 0 means ready to shoot
        self.__r_mod = 1.0  # gets bigger
        self.__p_mod = 1.0  # gets bigger
        self.__s_mod = 1.0  # gets bigger
        self.gun = Gun((self.x, self.y), s, t, tower_colors[self.t_num], self.level)
        self.upgrade_cost = 10
        self.follow_mouse = False
        self.show_r = False

    def color(self): return tower_colors[self.t_num]

    def cooldown(self): return enums.tower_cooldown[self.t_num] * self.__c_mod

    def range(self): return (enums.tower_range[self.t_num] * self.__r_mod * self.size) + self.size / 2

    def power(self): return enums.tower_power[self.t_num] * self.__p_mod

    def speed(self): return enums.tower_speed[self.t_num] * self.__s_mod

    def t_type(self): return enums.TowerType(self.t_num)

    def pos(self): return self.x, self.y

    def render(self, surf):
        if self.t_num == 0 or self.t_num == 7:  # PATH = 7, ZEROTOWER = 0
            pass
        else:
            pygame.draw.circle(surf, self.color(), self.box.center, self.size // 2, 4)
            self.gun.render(surf)
            if self.show_r:
                pygame.draw.circle(surf, red, self.box.center, int(self.range()), 1)

    def update(self, enemies, on_screen_shots, register):
        if self.t_num != 0 and self.t_num != 7:
            aim_spot = (0, 0)
            for e in enemies:
                if is_in_circle(e.center(), self.box.center, self.range()):
                    aim_spot = e.pos()
                    if self.coolness <= 0:
                        on_screen_shots.append(Shot(self.box.center, e.id, self.color(), self.speed(), self.power()))
                        register(on_screen_shots[len(on_screen_shots) - 1])  # register this bullet to be drawn
                        if self.t_num == 1:
                            on_screen_shots[len(on_screen_shots) - 1].poison = True
                        if self.t_num == 2:
                            on_screen_shots[len(on_screen_shots) - 1].ice = True
                        self.coolness = self.cooldown()
                    break
            if self.coolness > 0:
                self.coolness -= 1
            # point at the first enemy in range
            self.gun.update(aim_spot)

    def move(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.gun.x = pos[0]
        self.gun.y = pos[1]
        self.box = pygame.Rect((self.x, self.y), (self.size, self.size))

    def is_in(self, pos):
        if self.x < pos[0] < self.x + self.size:
            if self.y < pos[1] < self.y + self.size:
                return True
        return False

    def upgrade(self):
        self.__c_mod -= 0.1  # gets smaller
        self.__r_mod += 2.0  # gets bigger
        self.__p_mod += 1.0  # gets bigger
        self.__s_mod += 0.5  # gets bigger
        self.upgrade_cost *= 2
        self.level += 1

    def show_range(self, mouse):
        if self.is_in(mouse):
            self.show_r = True
        else:
            self.show_r = False
