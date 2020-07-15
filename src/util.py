import os
import pygame as pg
import math
IMG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'res', 'img')) + os.sep


def load_sprite_dictionary(folder, colorkey):
    """Loads a dictionary where key = file name, and value is a Sprite"""
    path = IMG_PATH + folder
    ret = {}
    fnames = os.listdir(path)  # get filenames
    for i in range(len(fnames)):
        ret[fnames[i].replace('.png', '')] = load_image(f"{folder}{os.sep}{fnames[i]}", colorkey)
    return ret


def load_image(fname, colorkey=None):
    try:
        image = pg.image.load(IMG_PATH + fname)
    except pg.error as message:
        print('Cannot load image:', fname)
        raise SystemExit(message)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pg.RLEACCEL)
            image = image.convert_alpha()
    else:
        image = image.convert()
    return image


def rot_center(image, rect, angle):
    """rotate an image while keeping its center
    returns an image and its rectangle"""
    rot_image = pg.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect


def distance(target, obj):
    return math.sqrt((obj.x - target.x)**2 + (obj.y - target.y) ** 2)


def angle_to(target, obj):
    """Return angle between TARGET and OBJ (Mind the order!) in RADIANS"""
    return math.atan2((target.y - obj.y), (target.x - obj.x))
