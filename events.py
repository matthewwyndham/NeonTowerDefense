import pygame

listeners = []


def init():
    pygame.key.set_repeat(20, 20)


def check():
    global listeners
    for e in pygame.event.get():
        for l in listeners:
            l(e)


def register(li):
    global listeners
    if li not in listeners:
        listeners.append(li)


def remove(li):
    global listeners
    if li in listeners:
        listeners.remove(li)
