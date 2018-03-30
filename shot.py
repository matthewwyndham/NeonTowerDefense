import pygame


# check for this outside the class:
# self.alive -> if this shot is dead, display an explosion at it's location and delete it from the list
class Shot:
    def __init__(self, pos, target, color, speed, power):
        self.x = pos[0]
        self.y = pos[1]
        self.target = target  # id of enemy
        self.color = color
        self.speed = speed
        self.power = power
        self.alive = True

    def pos(self): return self.x, self.y

    def end(self, enemies):
        target_pos = enemies[self.target].center()
        if self.speed == 0:
            return target_pos
        else:
            end = self.x, self.y
            if target_pos[0] < self.x:
                end[0] -= 2
            else:
                end[0] += 2
            if target_pos[1] < self.y:
                end[1] -= 2
            else:
                end[1] += 2
            return end

    def render(self, surf, enemies):
        pygame.draw.line(surf, self.color, self.pos, self.end(enemies), 3)

    def update(self, enemies):
        if self.target < len(enemies):
            e = enemies[self.target]
            if e.box().collidepoint(self.x, self.y):
                e.damage(self.power)
                self.alive = False
        else:
            self.target -= 1

    def kill(self):
        self.alive = False
