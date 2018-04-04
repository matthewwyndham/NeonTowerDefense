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
        self.temptarget = pos
        self.lazer_counter = 0
        self.poison = False
        self.ice = False

    def pos(self): return self.x, self.y

    def end(self, enemies):
        target_pos = enemies[self.target].center()
        if self.speed == 0:
            return target_pos
        else:
            endx = self.x
            endy = self.y
            if target_pos[0] < self.x:
                endx -= 2
            else:
                endx += 2
            if target_pos[1] < self.y:
                endy -= 2
            else:
                endy += 2
            end = endx, endy
            return end

    def render(self, surf):
        pygame.draw.line(surf, self.color, (self.x, self.y), self.temptarget, 3)

    def move_towards(self, pos):
        if self.x < pos[0]:
            self.x += self.speed
        if self.x > pos[0]:
            self.x -= self.speed
        if self.y < pos[1]:
            self.y += self.speed
        if self.y > pos[1]:
            self.y -= self.speed

    def update(self, enemies):
        if self.target < len(enemies):
            e = enemies[self.target]
            self.temptarget = self.end(enemies)
            self.move_towards(e.center())
            if e.box().collidepoint(self.x, self.y):
                e.damage(self.power)
                if self.poison:
                    e.poisoned = True
                if self.ice:
                    e.iced = True
                self.alive = False
            if self.speed == 0:
                self.lazer_counter += 1
                if self.lazer_counter > 5:
                    e.damage(self.power)
                    self.alive = False
        else:
            self.target -= 1
        if self.target < 0:
            self.alive = False
            self.temptarget = (0, 0)

    def kill(self):
        self.alive = False
