import pygame as pg
from random import randint
import os
SFX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'res', 'sfx')) + os.sep


class SoundPack:
    def __init__(self, folder):
        path = SFX_PATH + folder
        filenames = os.listdir(path)
        self.sounds = []
        for name in filenames:
            self.sounds.append(load_sound(f"{folder}{os.sep}{name}"))
        self.cur = 0
        self._last = len(self.sounds) - 1  # -1 to get the proper subscript for a list

    def _increment(self):
        self.cur += 1
        if self.cur >= len(self.sounds):
            self.cur = 0
        return self.cur

    def set_volume(self, vol: float):
        """From 0.0 to 1.0"""
        assert 1 > vol > 0, "Volume must be in the range from 0 to 1!"
        for el in self.sounds:
            el.set_volume(vol)

    def play_next(self):
        """Plays the next sound"""
        self._increment()
        self.sounds[self.cur].play()

    def play_random(self, loops=0, maxtime=0, fade_ms=0):
        """Plays the random sound (doesn't increment the counter)"""
        self.sounds[randint(0, self._last)].play(loops, maxtime, fade_ms)
        
    def play(self, loops=0, maxtime=0, fade_ms=0):  # Allows us to use pack where sound is expected
        self.play_random(loops, maxtime, fade_ms)
        
    def stop(self, fadeout_ms=0):
        for el in self.sounds:
            el.fadeout(fadeout_ms)
        
        
def load_sound(fname):
    try:
        sound = pg.mixer.Sound(SFX_PATH + fname)
    except pg.error as message:
        raise SystemExit(message)
    return sound
