from random import randint
from src.animation import *


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


def load_animations_dictionary(folder, image_square, pics_on_sheet, colorkey, *args):
    """Returns a dictionary where key = file name and value is an Animation"""
    path = IMG_PATH + folder
    ret = {}  # create a dictionary to store animations
    fnames = os.listdir(path)  # get filenames
    timings = get_timings(path, pics_on_sheet)  # attempt to get animation timings for the folder
    if TIMINGS_FILENAME in fnames:
        fnames.remove(TIMINGS_FILENAME)
    for i in range(len(fnames)):  # for every file
        sh = Spritesheet(f"{folder}/{fnames[i]}", colorkey)  # open a spritesheet, get the colorkey
        images = sh.load_strip(image_square, pics_on_sheet)  # load a list of sprites from the sheet
        anim = SpriteAnim((images, timings), *args)  # Create a new Animation with these args
        ret[fnames[i].replace('.png', '')] = anim  # add an entry to the dict
        # Add this animation to a dictionary + direction (e.g. 'ld' = left-down (tuple))
    return ret


def load_sprite_dictionary(folder, colorkey):
    "Loads a dictionary where key = file name, and value is a Sprite"
    path = IMG_PATH + folder
    ret = {}
    fnames = os.listdir(path)  # get filenames
    for i in range(len(fnames)):
        ret[fnames[i].replace('.png', '')] = load_image(f"{folder}{os.path.sep}{fnames[i]}", colorkey)
    return ret


def load_animation_from_table(folder: str, filename: str,
                              img_size_x: int, img_size_y: int,
                              colorkey=None,
                              frames_to_skip=DEFAULT_TIMING,
                              timings_filename=TIMINGS_FILENAME, *tags) -> SpriteAnim:
    """returns SpriteAnim"""
    sheet = Spritesheet(f'{folder}{SEP}{filename}', colorkey)  # load a spritesheet
    frames = sheet.load_table(img_size_x, img_size_y)  # get a list of frames
    timings = get_timings(f"{IMG_PATH}{folder}", len(frames), fname=timings_filename, frames_to_skip=frames_to_skip)
    return SpriteAnim((frames, timings), *tags)
