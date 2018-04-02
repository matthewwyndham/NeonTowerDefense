from enum import Enum


class Terrain(Enum):
    PATH = 0
    GROUND = 1
    OBSTRUCTED = 2
    BOOST = 3
    EMPTY = 4
    PLAYBUTTON = 5


class TowerType(Enum):
    ZEROTOWER = 0
    POISON = 1
    ICE = 2
    FAST = 3
    STRONG = 4
    LASER = 5
    BOOSTER = 6
    PATH = 7  # this is to take the place of paths in the tower list so that users can't put stuff there


#                  0    1    2    3    4    5    6    7
tower_cooldown = [ 0,  20,  20,  10,  20,   3,   0,   0]
tower_range    = [ 0,   3,   3,   3,   3,   5,   1,   0]  # number of cells it can shoot
tower_power    = [ 0,   5,   5,   5,  15,   1,   0,   0]
tower_speed    = [ 0,  10,  10,  10,   9,   0,   0,   0]  # speed of the projectiles, laser tower is a line
tower_cost     = [ 0, 100, 100, 100, 100, 100, 100,   0]


class EnemyType(Enum):
    ZEROENEMY = 0
    STRONG = 1
    FAST = 2
    GROUP = 3
    RESIST = 4


enemy_speed  = [0,  2,  7, 4, 4]
enemy_health = [0, 35, 14, 9, 9]

