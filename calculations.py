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


def is_in_circle(point, center, radius):
    x, y = point[0], point[1]
    cx, cy = center[0], center[1]
    return (x - cx)**2 + (y - cy)**2 < radius**2