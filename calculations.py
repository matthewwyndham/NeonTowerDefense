import math


def find_cell(m_pos, menu_width, cell_size, width):
    x = m_pos[0] - menu_width
    if x < 0:
        return -1
    x = int(x / cell_size)
    y = int(m_pos[1] / cell_size)
    return x + (y * int((width - menu_width) / cell_size))


def find_neighbors(cell, num_cells, cells_per_line):
    neighbors = []
    # 0 through cells_per_line -1 have no up neighbor
    if cell >= cells_per_line:
        neighbors.append(cell - cells_per_line)
    # cell % cells_per_line == 0 have no left neighbor
    if cell % cells_per_line != 0:
        neighbors.append(cell - 1)
    # cell % cells_per_line == cells_per_line -1 have no right neighbor
    if cell % cells_per_line != cells_per_line - 1:
        neighbors.append(cell + 1)
    # num_cells - cells_per_line through num_cells -1 have no down neighbor
    if cell < num_cells - cells_per_line:
        neighbors.append(cell + cells_per_line)
    return neighbors


def get_distance(p1, p2):
    x, y = p1[0], p1[1]
    xx, yy = p2[0], p2[1]
    return math.sqrt(((x - xx) ** 2) + ((y - yy) ** 2))


def is_in_circle(point, center, radius):
    x, y = point[0], point[1]
    cx, cy = center[0], center[1]
    return (x - cx)**2 + (y - cy)**2 < radius**2