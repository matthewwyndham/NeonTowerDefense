import pygame
import display
import events
import levels
from towers import Tower
from cell import Cell
from colors import *
from enums import *
from calculations import *
from textbox import Textbox
from resource import Resource

pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('Century Gothic', 18)

screen_width = 800
screen_height = 600
cell_size = 40
menu_width = 200
playfield_w = int((screen_width - menu_width) / cell_size)
playfield_h = int(screen_height / cell_size)
background_line_width = 1

display.init(screen_width, screen_height, cell_size, menu_width, playfield_w, playfield_h, background_line_width)
events.init()

# TODO: iterate for every level
current_level = levels.level_1
current_waves_list = levels.level_1_waves

level_number = 1
wave_number = 0
heart_number = 20
heart_max = heart_number
money = Resource()
victorious = False

# clean up the level
for i in range(len(current_level) - 1):
    current_level[i] = Terrain(current_level[i])

# locations for towers, color can be changed by changing the terrain type
cells = []
for i in range(playfield_w * playfield_h):
    x = int(i % playfield_w) * cell_size + menu_width
    y = int(i / playfield_w) * cell_size
    cells.append(Cell(i, x, y, cell_size, current_level[i]))
    display.register(cells[i])

# the path of positions that enemies must follow
# they should start at (-cell_size, 0) so they walk onto the screen
# then they move to the next square at the end of the path and make you lose a heart
path = []  # a collection of tuples (x, y) for enemies to follow
for i in range(len(cells)):
    if cells[i].t == Terrain.PATH:
        path.append((cells[i].x, cells[i].y))

# towers have their own list that mirrors cells, can't place in path cells
towers = []
for i in range(len(cells)):
    c = cells[i]
    if c.t == Terrain.PATH:
        towers.append(Tower(i, c.x, c.y, cell_size, TowerType.PATH.value))  # users can't replace this
        display.register(towers[len(towers) - 1])
    else:
        towers.append(Tower(i, c.x, c.y, cell_size, TowerType.ZEROTOWER.value))  # users can replace this
        display.register(towers[len(towers) - 1])

# enemies
enemies = []

# menu objects for buying and placing
# position should be relative to cell_size
menu = []
# 0-1 ; Title
menu.append(Textbox((6, 6), dark(red), font, "Neon Tower Defence"))
display.register(menu[0])
menu.append(Textbox((5, 5), text_color, font, "Neon Tower Defence"))
display.register(menu[1])
# 2-4 ; Level
playbutton = Cell(len(menu), cell_size * 3, cell_size, cell_size, Terrain.PLAYBUTTON)
level_active = False


# this function is part of the menu: playbutton
def start_level(e):
    global level_active, menu, wave_number
    if not level_active:
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                m_pos = pygame.mouse.get_pos()
                if find_cell(m_pos, menu_width, cell_size, screen_width) == -1:
                    if menu[2].is_in(m_pos):
                        level_active = True
                        display.remove(menu[2])
                        display.remove(menu[3])
                        display.register(menu[4])
                        initialize_wave()


events.register(start_level)

menu.append(playbutton)
display.register(menu[2])
menu.append(Textbox((5, cell_size + 5), text_color, font, "Start Level"))
display.register(menu[3])
menu.append(Textbox((5, cell_size + 5), text_color, font, "Level: " + str(level_number)))
# display.register(menu[4])
# 5 ; Wave
menu.append(Textbox((5, cell_size * 2 + 5), text_color, font, "Wave: " + str(wave_number)))
display.register(menu[5])
# 6 ; Hearts
menu.append(Textbox((5, cell_size * 3 + 5), text_color, font, "Hearts: " + str(heart_number) + "/" + str(heart_max)))
display.register(menu[6])
# 7 ; Money
menu.append(Textbox((5, cell_size * 4 + 5), text_color, font, "Money: " + str(money.get())))
display.register(menu[7])
# 8 ; Kill Count
# 9 ; Towers
# - 1 ; POISON
# - 2 ; ICE
# - 3 ; FAST
# - 4 ; STRONG
# - 5 ; LASER
# - 6 ; BOOSTER

# tracks the bullets and draws them, allows them to collide with enemies and cause damage
on_screen_shots = []

run = True


def quit_handler(e):
    global run
    if e.type == pygame.QUIT:
        run = False
    elif e.type == pygame.KEYUP:
        if e.key == pygame.K_ESCAPE:
            run = False


events.register(quit_handler)


# TODO: change this function to upgrade placed towers
def mouse_control(e):
    if e.type == pygame.MOUSEBUTTONDOWN:
        if e.button == 1:
            c = find_cell(pygame.mouse.get_pos(), menu_width, cell_size, screen_width)
            if c != -1:
                # cells[c].t = Terrain((cells[c].t.value + 1) % (Terrain.__len__()))
                towers[c].t_num = (towers[c].t_num + 1) % TowerType.__len__()


events.register(mouse_control)


def initialize_wave():
    global enemies, wave_number, level_active, victorious
    wave_number += 1  # we are showing the user that this is wave one, but we are accessing wave 0 in the list
    if wave_number - 1 < len(current_waves_list):
        pass
    else:
        level_active = False
        victorious = True



while run:
    # if level is over, show the play button
    # display.register(menu[2])
    # display.register(menu[3])
    # increment the level number
    # update the level number box (menu[4])

    if len(enemies) == 0:
        wave_number += 1
        initialize_wave()

    # update everything that needs updating
    if level_active:
        for t in towers:
            t.update(enemies, on_screen_shots, display.register)
        for e in enemies:
            e.update(path)
            if not e.alive:
                enemies.remove(e)
                # break  # may need a break here and there...
            if e.hurts:
                heart_number -= 1
                enemies.remove(e)
                # break  # TODO: may need to use break here.
        for s in on_screen_shots:
            s.update(enemies)

    # dynamically register all bullets
    # for s in on_screen_shots:
    #     display.register(s)

    events.check()
    display.update()
    clock.tick(60)
exit(0)
