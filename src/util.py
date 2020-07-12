import pygame as pg
import os
SAFEZONE_MULTIPLIER = 3  # the MINIMUM amount of the times the object
# can fit into the distance between it and newly spawned object
DEFAULT_TIMING = 3  # The time between frames in animations
TIMINGS_FILENAME = 'timings.txt'
SEP = os.path.sep
IMG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'res', 'img')) + SEP
SFX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'res', 'sfx')) + SEP


def load_image(fname, colorkey=None):
    try:
        image = pg.image.load(IMG_PATH+fname)
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


def load_sound(fname):
    try:
        sound = pg.mixer.Sound(SFX_PATH + fname)
    except pg.error as message:
        raise SystemExit(message)
    return sound


def rot_center(image, rect, angle):
    """rotate an image while keeping its center
    returns an image and its rectangle"""
    rot_image = pg.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect


def get_timings(path, num_frames=0, *, fname=TIMINGS_FILENAME, frames_to_skip=DEFAULT_TIMING):
    """gets timings from the file. If you don't specify the amount, the file won't be checked for errors
    If no file is present, the function will return default generated timings based on the arguments provided"""
    try:
        f = open(f'{path}{SEP}{fname}')  # try to get the file
        timings_text = f.read().split(';')
        f.close()
        timings = tuple(int(i) for i in timings_text)  # convert to numeric list
        if num_frames:
            if len(timings) != num_frames:
                raise IndexError(f"Timings don't match images in {path}")
    except FileNotFoundError:  # If not found, use default
        print(f"Haven't found timings in {path} , using default")
        if num_frames <= 0:
            raise ValueError("Wrong amount of frames supplied")
        timings = tuple([frames_to_skip] * num_frames)
    return timings


def generate_timings(num_frames: int, delay: int):
    return tuple([delay] * num_frames)


def load_anim(folder, colorkey=None, timings_fname=TIMINGS_FILENAME):
    """Loads images from the specified folder and returns a list of pygame image objects and their timings
    returns a tuple of images and timings"""
    path = IMG_PATH+folder
    filenames = os.listdir(path)
    if timings_fname in filenames:
        filenames.pop(filenames.index(timings_fname))
    frames_cnt = len(filenames)
    timings = get_timings(path, frames_cnt, fname=timings_fname)
    imgs = []
    for fname in filenames:
        imgs.append(load_image(f'{folder}{SEP}{fname}', colorkey))
    return imgs, timings


def upscale_image(img, coefficient):
    """returns upscaled image. The argument is unchanged"""
    ret = img
    if coefficient % 2 == 0:
        while coefficient != 1:
            coefficient //= 2
            ret = pg.transform.scale2x(ret)
    else:
        base_rect = img.get_rect()
        ret = pg.transform.smoothscale(img, (base_rect.width * coefficient, base_rect.height * coefficient))
    return ret


def upscale_anim(sprite_list, coefficient):
    """returns a list of images and their rectangles
    sprite_list is a list of pygame.sprites"""
    for i in range(len(sprite_list)):
        sprite_list[i] = upscale_image(sprite_list[i], coefficient)
    return sprite_list


def load_soundlist(folder):
    """loads a list of soundpack and returns it"""
    path = SFX_PATH+folder
    filenames = os.listdir(path)
    ret = []
    for name in filenames:
        ret.append(load_sound(f"{folder}{SEP}{name}"))
    return ret

