from src.util import *
from random import randint
from src.animation import *


class Spritesheet:
    def __init__(self, filename, colorkey=None):
        self.sheet = load_image(filename, colorkey)[0]
        self.colorkey = colorkey
        if self.colorkey == -1:
            self.colorkey = self.sheet.get_at((0, 0))

    def _convert(self, img):
        if self.colorkey is not None:
            img.set_colorkey(self.colorkey, pg.RLEACCEL)
            return img.convert_alpha()
        else:
            return img.convert()

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle):
        """Loads image from x,y,x+offset,y+offset"""
        rect = pg.Rect(rectangle)
        image = self._convert(pg.Surface(rect.size))
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


class SoundPack:
    def __init__(self, soundlist):
        self.sounds = soundlist
        self._i = 0

    def _increment(self):
        self._i += 1
        if self._i >= len(self.sounds):
            self._i = 0
        return self._i

    def set_volume(self, vol):
        """From 0.0 to 1.0"""
        for el in self.sounds:
            el.set_volume(vol)

    def get_random(self):
        return self.sounds[randint(0, len(self.sounds) - 1)]

    def get_next(self):
        self._increment()
        return self.sounds[self._i]

    def play_next(self):
        self._increment()
        self.sounds[self._i].play()

    def play_random(self):
        self.sounds[randint(0, len(self.sounds) - 1)].play()


def load_animations_dictionary(folder, pics_on_sheet, *args):
    path = IMG_PATH+folder
    ret = {}  # create a dictionary to store animations
    fnames = os.listdir(path)  # get filenames
    timings = get_timings(path, pics_on_sheet)  # attempt to get animation timings for the folder
    if TIMINGS_FILENAME in fnames:
        fnames.remove(TIMINGS_FILENAME)
    for i in range(len(fnames)):  # for every file
        sh = Spritesheet(f"{folder}/{fnames[i]}", -1)  # open a spritesheet, get the colorkey
        images = sh.load_strip((0, 0, 32, 32), pics_on_sheet)  # load a list of sprites from the sheet
        anim = SpriteAnim(None, (images, timings), *args)  # Create a new Animation with these args
        ret[fnames[i].replace('.png', '')] = anim
        # Add this animation to a dictionary + direction (e.g. 'ld' = left-down (tuple))
    return ret
