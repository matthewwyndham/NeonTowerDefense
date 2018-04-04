import pygame
import display
import events
import levels
import generic_renderables
from towers import Tower
from cell import Cell
from enemy import Enemy
from colors import *
from enums import *
from calculations import *
from textbox import Textbox
from resource import Resource

pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('Century Gothic', 18)
big_font = pygame.font.SysFont('Century Gothic', 22)

game_speed = 40
screen_width = 800
screen_height = 600
cell_size = 40
menu_item_height = cell_size / 2
menu_item_v_offset = cell_size / 2 + 5
menu_tower_v_offset = menu_item_height * 7 + menu_item_v_offset + 7
tower_spacing = 45
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
kill_counter = 0
heart_max = heart_number
money = Resource()
money.gain(250)
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
path = [cells[0].pos(), cells[1].pos(), cells[2].pos(), cells[3].pos(),
        cells[18].pos(), cells[33].pos(), cells[48].pos(), cells[63].pos(),
        cells[78].pos(), cells[93].pos(), cells[108].pos(), cells[123].pos(),
        cells[138].pos(), cells[153].pos(), cells[168].pos(), cells[183].pos(),
        cells[184].pos(), cells[185].pos(), cells[186].pos(), cells[187].pos(),
        cells[188].pos(), cells[173].pos(), cells[158].pos(), cells[143].pos(),
        cells[128].pos(), cells[113].pos(), cells[98].pos(), cells[99].pos(),
        cells[100].pos(), cells[101].pos(), cells[102].pos(), cells[117].pos(),
        cells[132].pos(), cells[147].pos(), cells[162].pos(), cells[177].pos(),
        cells[192].pos(), cells[207].pos(), cells[222].pos(), cells[223].pos(),
        cells[224].pos()
        ]  # a collection of tuples (x, y) for enemies to follow
# for i in range(len(cells)):
#     if cells[i].t == Terrain.PATH:
#         path.append((cells[i].x, cells[i].y))
#         if i+ playfield_w < len(cells):
#             if cells[i+1].t != Terrain.PATH:
#                 i += playfield_w

# towers have their own list that mirrors cells, can't place in path cells
towers = []
for i in range(len(cells)):
    c = cells[i]
    if c.t == Terrain.PATH:
        towers.append(Tower(i, c.x, c.y, cell_size, TowerType.PATH.value))  # users can't replace this
        #display.register(towers[len(towers) - 1])
    else:
        towers.append(Tower(i, c.x, c.y, cell_size, TowerType.ZEROTOWER.value))  # users can replace this
        #display.register(towers[len(towers) - 1])

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
playbutton = Cell(-4, cell_size * 3 + 5, cell_size, cell_size / 4 * 3, Terrain.PLAYBUTTON)
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
menu.append(Textbox((5, cell_size), text_color, big_font, "Start Level"))
display.register(menu[3])
menu.append(Textbox((5, cell_size), text_color, big_font, "Level: " + str(level_number)))
# display.register(menu[4])
# 5 ; Wave
menu.append(Textbox((5, menu_item_height * 2 + menu_item_v_offset), text_color, font, "Wave: " + str(wave_number)))
display.register(menu[5])
# 6 ; Hearts
menu.append(Textbox((5, menu_item_height * 3 + menu_item_v_offset), text_color, font, "Hearts: " + str(heart_number) + "/" + str(heart_max)))
display.register(menu[6])
# 7 ; Money
menu.append(Textbox((5, menu_item_height * 4 + menu_item_v_offset), text_color, font, "Money: " + str(money.get())))
display.register(menu[7])
# 8 ; Kill Count
menu.append(Textbox((5, menu_item_height * 5 + menu_item_v_offset), text_color, font, "Kills: " + str(kill_counter)))
display.register(menu[8])
# 9 ; Towers -------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
menu.append(Textbox((5, menu_item_height * 6 + menu_item_v_offset), dark(red), font, "Towers"))
display.register(menu[9])
box = generic_renderables.Box((2, menu_item_height * 6 + menu_item_v_offset + 22), (menu_width - 4, screen_height - (menu_item_height * 6 + menu_item_v_offset + 24)), dark(red))
menu.append(box)
display.register(menu[10])
# - 1 ; POISON -------------------------------------------------------------------------------------------
menu.append(Textbox((5, menu_tower_v_offset - 5), text_color, font, "Poison"))
display.register(menu[11])
menu.append(Textbox((5, menu_tower_v_offset + cell_size / 2 - 5), text_color, font,
                    "Cost: " + str(tower_cost[1])))
display.register(menu[12])
menu.append(Tower(-1, cell_size * 3, menu_tower_v_offset, cell_size, 1))
display.register(menu[13])
# - 2 ; ICE -------------------------------------------------------------------------------------------
menu.append(Textbox((5, tower_spacing * 1 + menu_tower_v_offset - 5), text_color, font, "Ice"))
display.register(menu[14])
menu.append(Textbox((5, tower_spacing * 1 + menu_tower_v_offset + cell_size / 2 - 5), text_color, font,
                    "Cost: " + str(tower_cost[2])))
display.register(menu[15])
menu.append(Tower(-1, cell_size * 3, tower_spacing * 1 + menu_tower_v_offset, cell_size, 2))
display.register(menu[16])
# - 3 ; FAST -------------------------------------------------------------------------------------------
menu.append(Textbox((5, tower_spacing * 2 + menu_tower_v_offset - 5), text_color, font, "Fast"))
display.register(menu[17])
menu.append(Textbox((5, tower_spacing * 2 + menu_tower_v_offset + cell_size / 2 - 5), text_color, font,
                    "Cost: " + str(tower_cost[3])))
display.register(menu[18])
menu.append(Tower(-1, cell_size * 3, tower_spacing * 2 + menu_tower_v_offset, cell_size, 3))
display.register(menu[19])
# - 4 ; STRONG -------------------------------------------------------------------------------------------
menu.append(Textbox((5, tower_spacing * 3 + menu_tower_v_offset - 5), text_color, font, "Strong"))
display.register(menu[20])
menu.append(Textbox((5, tower_spacing * 3 + menu_tower_v_offset + cell_size / 2 - 5), text_color, font,
                    "Cost: " + str(tower_cost[4])))
display.register(menu[21])
menu.append(Tower(-1, cell_size * 3, tower_spacing * 3 + menu_tower_v_offset, cell_size, 4))
display.register(menu[22])
# - 5 ; LASER -------------------------------------------------------------------------------------------
menu.append(Textbox((5, tower_spacing * 4 + menu_tower_v_offset - 5), text_color, font, "Laser"))
display.register(menu[23])
menu.append(Textbox((5, tower_spacing * 4 + menu_tower_v_offset + cell_size / 2 - 5), text_color, font,
                    "Cost: " + str(tower_cost[5])))
display.register(menu[24])
menu.append(Tower(-1, cell_size * 3, tower_spacing * 4 + menu_tower_v_offset, cell_size, 5))
display.register(menu[25])
# - 6 ; BOOSTER -------------------------------------------------------------------------------------------
# menu.append(Textbox((5, tower_spacing * 5 + menu_tower_v_offset - 5), text_color, font, "Boost"))
# display.register(menu[26])
# menu.append(Textbox((5, tower_spacing * 5 + menu_tower_v_offset + cell_size / 2 - 5), text_color, font,
#                     "Cost: " + str(tower_cost[6])))
# display.register(menu[27])
# menu.append(Tower(-1, cell_size * 3, tower_spacing * 5 + menu_tower_v_offset, cell_size, 6))
# display.register(menu[28])


# update the menu items
def update_menu():
    global menu, wave_number, heart_number, heart_max, money, kill_counter
    menu[5].text = "Wave: " + str(wave_number)
    menu[6].text = "Hearts: " + str(heart_number) + "/" + str(heart_max)
    menu[7].text = "Money: " + str(money.get())
    menu[8].text = "Kills: " + str(kill_counter)


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

mouse_tower = Tower(-1, -cell_size, -cell_size, cell_size, 0)
display.register(mouse_tower)

# TODO: change this function to upgrade placed towers
def mouse_control(e):
    global mouse_tower, menu_width, cell_size, screen_width, money, towers, display, cells, playfield_w
    if e.type == pygame.MOUSEBUTTONDOWN:
        m_pos = pygame.mouse.get_pos()
        if e.button == 1:
            c = find_cell(m_pos, menu_width, cell_size, screen_width)
            if c != -1:
                if mouse_tower.follow_mouse:
                    if (towers[c].t_num == TowerType.ZEROTOWER.value) and (cells[c].t != Terrain.OBSTRUCTED):
                        if money.can_spend(100):
                            # cells[c].t = Terrain((cells[c].t.value + 1) % (Terrain.__len__()))
                            # towers[c].t_num = (towers[c].t_num + 1) % TowerType.__len__()
                            towers[c] = Tower(c, towers[c].x, towers[c].y, cell_size, mouse_tower.t_num)
                            display.register(towers[c])
                            display.remove(mouse_tower)
                            mouse_tower.follow_mouse = False
                            money.spend(100)
                # else:
                #     for n in find_neighbors(cells[c].identity, len(cells), playfield_w):
                #         cells[n].t = Terrain.OBSTRUCTED
            if c == -1:
                if not mouse_tower.follow_mouse:
                    for item in menu:
                        if item.identity == -1:
                            if item.is_in(m_pos):
                                mouse_tower = Tower(-1, m_pos[0], m_pos[1], cell_size, item.t_num)
                                display.register(mouse_tower)
                                mouse_tower.follow_mouse = True
                else:
                    display.remove(mouse_tower)
                    mouse_tower.follow_mouse = False




events.register(mouse_control)


def initialize_wave():
    global enemies, wave_number, level_active, victorious, level_number, cell_size
    wave_number += 1  # we are showing the user that this is wave one, but we are accessing wave 0 in the list
    if wave_number - 1 < len(current_waves_list):
        counter = 0
        for num in range(len(current_waves_list[wave_number - 1])):
            enemies.append(Enemy(counter, cell_size / 2, current_waves_list[wave_number - 1][num], level_number,
                                 wave_number, (menu_width, -cell_size - (counter * 30))))
            display.register(enemies[counter])
            print(current_waves_list[wave_number - 1][num])
            counter += 1
    else:
        level_active = False
        victorious = True



while run:
    m_pos = pygame.mouse.get_pos()

    update_menu()

    # if level is over, show the play button
    # display.register(menu[2])
    # display.register(menu[3])
    # increment the level number
    # update the level number box (menu[4])

    if len(enemies) == 0 and level_active:
        initialize_wave()

    if mouse_tower.follow_mouse:
        mouse_tower.move(pygame.mouse.get_pos())

    for t in towers:
        t.show_range(m_pos)

    # update everything that needs updating
    if level_active:
        for t in towers:
            t.update(enemies, on_screen_shots, display.register)
        for e in enemies:
            e.update(path)
            if not e.alive:
                display.remove(e)
                enemies.remove(e)
                kill_counter += 1
                money.gain(e.value())
                break
            if e.hurts:
                heart_number -= 1
                enemies.remove(e)
                display.remove(e)
                break
        for s in on_screen_shots:
            s.update(enemies)
            if not s.alive:
                display.remove(s)
                on_screen_shots.remove(s)
            # s.update(enemies)

    # dynamically register all bullets
    # for s in on_screen_shots:
    #     display.register(s)

    events.check()
    display.update()
    clock.tick(game_speed)
exit(0)
