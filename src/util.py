import pygame as pg
import sys
import json
import platform

def load_sprite(name, colorkey=None):
    fullname = "../res/img/" + name
    try:
        image = pg.image.load(fullname)
    except pg.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self): pass

    if not pg.mixer:
        return NoneSound()
    fullname = "../res/sound/" + name
    try:
        sound = pg.mixer.Sound(fullname)
    except pg.error as message:
        print('Cannot load sound:', name)
        raise SystemExit(message)
    return sound


def toggle_fullscreen():
    if platform.system() == 'Linux':
        pg.display.toggle_fullscreen()
    else:
        game.screen = pg.display.set_mode((game.screen_width, game.screen_height))
