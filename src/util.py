import pygame as pg
import platform
import os

DEFAULT_TIMING = 3
TIMINGS_FILENAME = 'timings.txt'


def load_image(fname, colorkey=None):
    try:
        image = pg.image.load(f"../res/img/{fname}")
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
    return image, image.get_rect()


def load_sound(fname):
    try:
        sound = pg.mixer.Sound(f"../res/sfx/{fname}")
    except pg.error as message:
        raise SystemExit(message)
    return sound


def toggle_fullscreen():
    """suppported only on linux"""
    if platform.system() == 'Linux':
        pg.display.toggle_fullscreen()


def rot_center(image, rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pg.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect


def get_timings(path, amount, fname=TIMINGS_FILENAME):
    try:
        f = open(f'{path}/{fname}')  # try to get the file
        timings_text = f.read().split(';')
        f.close()
        timings = tuple(int(i) for i in timings_text)  # convert to numeric list
        if len(timings) != amount:
            raise IndexError(f"Timings don't match images in {path}")
    except FileNotFoundError:  # If not found, use default
        print(f"Haven't found timings in {path} , using default")
        timings = tuple([DEFAULT_TIMING] * amount)  # create a default timings list
    return timings


def load_anim(folder, colorkey=None, timings_fname=TIMINGS_FILENAME):
    """Loads images from the specified folder and returns a list of pygame image objects and their timings"""
    path = f'../res/img/{folder}'
    filenames = os.listdir(path)
    if timings_fname in filenames:
        filenames.pop(filenames.index(timings_fname))
    frames_cnt = len(filenames)
    timings = get_timings(path, frames_cnt, timings_fname)
    imgs = []
    # Make the timings list display frames to switch the image
    _sum = 0
    frames = []
    for i in timings:
        frames.append(_sum)  # fill the frames list
        _sum += i  # increase the frame
        # TODO: Test for logic errors
    for fname in filenames:
        imgs.append(load_image(f'{folder}/{fname}', colorkey)[0])
    return imgs, tuple(frames)


def upscale_anim(anim, coefficient=2.0):
    """upscale every frame in a list of images"""
    if coefficient % 2 == 0:
        while coefficient != 1:
            coefficient //= 2
            for i in range(len(anim)):
                anim[i] = pg.transform.scale2x(anim[i])
    else:
        for i in range(len(anim)):
            base_rect = anim[i].get_rect()
            anim[i] = pg.transform.smoothscale(anim[i], (base_rect.width * coefficient, base_rect.height * coefficient))
    return anim


def load_soundlist(folder):
    path = f'../res/sfx/{folder}'
    filenames = os.listdir(path)
    ret = []
    for name in filenames:
        ret.append(load_sound(f"{folder}/{name}"))
    return ret
