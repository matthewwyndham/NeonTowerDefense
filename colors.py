def dark(color):
    return color[0] / 2, color[1] / 2, color[2] / 2

def light(color):
    r = color[0] + 100
    g = color[1] + 100
    b = color[2] + 100
    if r > 255: r = 255
    if g > 255: g = 255
    if b > 255: b = 255
    return r, g, b

white = 255, 255, 255
black = 0, 0, 0
blue = 0, 0, 255
red = 255, 0, 0
green = 0, 255, 0

poison = 50, 200, 50
ice = 0, 0, 255
fast = 170, 170, 170
strong = 255, 0, 0
laser = 100, 200, 0
boost = 120, 50, 240

background_line_color = 25, 25, 100
background_color = 10, 10, 15

text_color = 200, 200, 225

terrain_colors = [dark(green), black, dark(red), light(background_line_color), dark(white), dark(blue)]
tower_colors = [black, poison, ice, fast, strong, laser, boost, white]
enemy_colors = [white, blue, black, background_line_color, red]
