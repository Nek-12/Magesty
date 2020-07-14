from abc import ABCMeta, abstractmethod
import os
import pygame as pg
import math
from random import randint, choice
SAFEZONE_MULTIPLIER = 3  # the MINIMUM amount of the times the object
# can fit into the distance between it and newly spawned object
DEFAULT_TIMING = 3  # The time between frames in animations
TIMINGS_FILENAME = 'timings.txt'
SEP = os.path.sep
IMG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'res', 'img')) + SEP
SFX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'res', 'sfx')) + SEP


class Animation(metaclass=ABCMeta):
    """A class that conveniently switches frames by a call.
    Usage: call self.animation.tick(owner) every frame -> frame changes if necessary"""

    def __init__(self):
        self.ended = False

    @abstractmethod
    def tick(self, owner):
        if self.ended:
            raise RuntimeError(f"Called tick after the animation ended, owner: {owner}")

    @abstractmethod
    def restart(self, owner):
        self.ended = False


class SpriteAnim(Animation):
    def __init__(self, anim_and_timings, *tags):
        """animation=(frames list, timings list), tags include: 'loop', 'reverse'
        if reversed, the timings still must be supplied correctly"""
        super().__init__()
        if 'reverse' in tags:
            self.frames = reversed(anim_and_timings[0])
        else:
            self.frames = anim_and_timings[0]  # images
        self.looped = 'loop' in tags  # detect if the animation is looped
        self.base_image = self.frames[0]
        self.timings = anim_and_timings[1]
        self.rect = self.base_image.get_rect()
        self._i = 0  # animation counter
        self._cur = 0  # animation frame (skip the first)

    def rotate_frames(self, angle):
        """ANGLE IN DEGREES"""
        for i in range(len(self.frames)):
            self.frames[i] = rot_center(self.frames[i], self.rect, angle)[0]
        self.base_image, self.rect = rot_center(self.base_image, self.rect, angle)

    def upscale_frames(self, coefficient):
        self.frames = upscale_anim(self.frames, coefficient)
        self.base_image = self.frames[0]
        self.rect = self.base_image.get_rect()
        return self

    def set_frames(self, frames_list, are_reversed=False):
        if are_reversed:
            self.frames = reversed(frames_list)
        else:
            self.frames = frames_list  # images
        self.base_image = self.frames[0]
        self.rect = self.base_image.get_rect()

    def restart(self, owner):
        super().restart(owner)
        self._i = 0
        self._cur = 1
        owner.image = self.base_image  # sets the frame to first
        return self

    def tick(self, owner):
        """Call tick every frame"""
        super().tick(owner)
        self.rect = owner.rect
        if self._cur >= len(self.frames):
            if self.looped:
                self.restart(owner)
                return True
            else:
                self.ended = True
                return False
        self._i += 1
        if self._i == self.timings[self._cur]:  # if the counter reached the value in the next position in the list
            self._i = 0
            owner.image = self.frames[self._cur]  # set the new frame
            self._cur += 1  # begin waiting for the next frame
            return True  # changed
        else:
            return False  # indicate no change


class RotatingAnim(Animation):
    """Animation that rotates the sprite"""

    # TODO: Add speedup/slowdown

    def __init__(self, image, d_alpha, to_alpha=360, *tags):
        """args include: 'loop', 'reverse'"""
        super().__init__()
        self._base_image = image
        self.rect = image.get_rect()
        mul = -1 * ('reversed' in tags)
        self.d_alpha = d_alpha * mul  # animation counter
        self.to_alpha = to_alpha * mul
        self.alpha = 0
        self.looped = 'loop' in tags  # detect if the animation is looped

    def restart(self, owner):
        super().restart(owner)
        self.alpha = 0
        owner.image = self._base_image

    def tick(self, owner):
        """Tick every frame"""
        super().tick(owner)
        self.rect = owner.rect
        if self.alpha >= self.to_alpha:
            if self.looped:
                self.restart(owner)
                return True
            else:
                self.ended = True
                return False
        self.alpha += self.d_alpha
        print(self.alpha)
        owner.image, owner.rect = rot_center(self._base_image, self._base_image.get_rect(), self.alpha)
        # TODO: Test collision handling
        return True  # indicate the change


# class BlinkingAnim(Animation):
#     """Blinks with the specified parameters"""
#     def __init__(self, owner, image, d_alpha, times=0, starting_alpha=0):
#         """If times = 0, then the animation works indefinitely"""
#         super().__init__(owner)
#         self.image = image
#         self.d_alpha = d_alpha
#         self.times = times
#         self._base_alpha = starting_alpha
#         self.alpha = starting_alpha
#         self._i = 0
#
#     def restart(self):
#         self.alpha = self._base_alpha


class Spritesheet:
    def __init__(self, filename, colorkey=None):
        self.sheet = load_image(filename, colorkey)
        self.colorkey = colorkey
        if self.colorkey == -1:
            self.colorkey = self.sheet.get_at((0, 0))

    def _convert(self, img):
        ret = img
        if self.colorkey is not None:
            ret.set_colorkey(self.colorkey, pg.RLEACCEL)
            return ret.convert_alpha()
        else:
            return ret.convert()

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle):
        """Loads image from left,top,width,height"""
        rect = pg.Rect(rectangle)
        image = self._convert(pg.Surface(rect.size))  # TODO: test for None and -1 colorkeys
        image.blit(self.sheet, (0, 0), rect)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects):
        """Loads multiple images, supply a list of coordinates"""
        return [self.image_at(rect) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count):
        """Loads a strip of images and returns them as a list"""
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups)

    def load_table(self, img_size_x, img_size_y):
        """Returns a list of animations from the spritesheet that contains several rows of images
        images must have same size"""
        sheet_rect = self.sheet.get_rect()
        w = sheet_rect.width
        h = sheet_rect.height
        if h % img_size_y != 0 or w % img_size_x != 0:
            raise ValueError("The spritesheet doesn't contain an integer number of images")
        columns = w // img_size_x
        rows = h // img_size_y
        x, y = 0, 0
        rects = []
        for i in range(rows):  # on every row, append rectangles
            x = 0
            for j in range(columns):  # append a rectangle
                rects.append((x, y, img_size_x, img_size_y))  # append a tuple
                x += img_size_x  # get to the next position
            y += img_size_y  # get to the next row
        return self.images_at(rects)


class SoundPack:
    def __init__(self, soundlist):
        self.sounds = soundlist
        self._i = 0

    def _increment(self):
        self._i += 1
        if self._i >= len(self.sounds):
            self._i = 0
        return self._i

    def set_volume(self, vol: float):
        """From 0.0 to 1.0"""
        assert 1 > vol > 0, "Volume must be in the range from 0 to 1!"
        for el in self.sounds:
            el.set_volume(vol)

    def get_random(self):
        return self.sounds[randint(0, len(self.sounds) - 1)]

    def get_next(self):
        """Get the next sound"""
        self._increment()
        return self.sounds[self._i]

    def play_next(self):
        """Plays the next sound"""
        self._increment()
        self.sounds[self._i].play()

    def play_random(self):
        """Plays the random sound (doesn't increment the counter)"""
        self.sounds[randint(0, len(self.sounds) - 1)].play()
        # -1 to get the proper subscript for a list

    def play(self):  # Allows us to use pack where sound is expected
        self.play_random()


def load_anim_dict_from_strips(folder, image_rect, pics_on_sheet, colorkey, *args):
    """Returns a dictionary where key = file name and value is an Animation"""
    path = IMG_PATH + folder
    ret = {}  # create a dictionary to store animations
    fnames = os.listdir(path)  # get filenames
    timings = get_timings(path, pics_on_sheet)  # attempt to get animation timings for the folder
    if TIMINGS_FILENAME in fnames:
        fnames.remove(TIMINGS_FILENAME)
    for i in range(len(fnames)):  # for every file
        sh = Spritesheet(f"{folder}/{fnames[i]}", colorkey)  # open a spritesheet, get the colorkey
        images = sh.load_strip(image_rect, pics_on_sheet)  # load a list of sprites from the sheet
        anim = SpriteAnim((images, timings), *args)  # Create a new Animation with these args
        ret[fnames[i].replace('.png', '')] = anim  # add an entry to the dict
        # Add this animation to a dictionary + direction (e.g. 'ld' = left-down (tuple))
    return ret


def load_sprite_dictionary(folder, colorkey):
    """Loads a dictionary where key = file name, and value is a Sprite"""
    path = IMG_PATH + folder
    ret = {}
    fnames = os.listdir(path)  # get filenames
    for i in range(len(fnames)):
        ret[fnames[i].replace('.png', '')] = load_image(f"{folder}{os.path.sep}{fnames[i]}", colorkey)
    return ret


def load_anim_from_table(folder: str, filename: str,
                         img_size_x: int, img_size_y: int,
                         colorkey=None,
                         frames_to_skip=DEFAULT_TIMING,
                         timings_filename=TIMINGS_FILENAME, *tags) -> SpriteAnim:
    """returns SpriteAnim"""
    sheet = Spritesheet(f'{folder}{SEP}{filename}', colorkey)  # load a spritesheet
    frames = sheet.load_table(img_size_x, img_size_y)  # get a list of frames
    timings = get_timings(f"{IMG_PATH}{folder}", len(frames), fname=timings_filename, frames_to_skip=frames_to_skip)
    return SpriteAnim((frames, timings), *tags)


def generate_animation_dict(anim_list: list, timings_each: list):
    return {
        'u': SpriteAnim((anim_list[0:3], timings_each), 'loop'),
        'r': SpriteAnim((anim_list[3:6], timings_each), 'loop'),
        'd': SpriteAnim((anim_list[6:9], timings_each), 'loop'),
        'l': SpriteAnim((anim_list[9:12], timings_each), 'loop')
    }


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
    path = IMG_PATH + folder
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
    path = SFX_PATH + folder
    filenames = os.listdir(path)
    ret = []
    for name in filenames:
        ret.append(load_sound(f"{folder}{SEP}{name}"))
    return ret


def distance(target, obj):
    return math.sqrt((obj.x - target.x)**2 + (obj.y - target.y) ** 2)


def angle_to(target, obj):
    """Return angle between TARGET and OBJ (Mind the order!) in RADIANS"""
    return math.atan2((target.y - obj.y), (target.x - obj.x))
