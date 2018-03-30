import math


def find_cell(m_pos, menu_width, cell_size, width):
    x = m_pos[0] - menu_width
    if x < 0:
        return -1
    x = int(x / cell_size)
    y = int(m_pos[1] / cell_size)
    return x + (y * int((width - menu_width) / cell_size))


def get_distance(p1, p2):
    x, y = p1[0], p1[1]
    xx, yy = p2[0], p2[1]
    return math.sqrt(((x - xx) ** 2) + ((y - yy) ** 2))