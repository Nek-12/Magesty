import pygame
import sys
import json
from src.data import *
from src.object import *
from src.game import *


def load_sprite(name, colorkey=None):
    fullname = "../res/"+name
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
