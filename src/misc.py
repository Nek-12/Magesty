from src.util import*
from src.object import *


class Animation(pg.sprite.Sprite):
    """A class that conveniently switches frames by a call."""
    def __init__(self, anim_tuple, *args):
        """args include: 'loop', 'reverse' (WIP)"""
        super().__init__()
        self.image = anim_tuple[0][0]  # current image, begin with the first frame
        self.frames = anim_tuple[0]  # images
        self.timings = anim_tuple[1]
        self.rect = self.image.get_rect()
        self._i = 0  # animation counter
        self._cur = 1  # animation frame (skip the first)
        self.looped = 'loop' in args  # detect if the animation is looped
        self.ended = False

    def restart(self):
        self._i = 0
        self._cur = 1
        self.image = self.frames[self._cur]
        self.ended = False

    def tick(self, *args):
        """Tick every frame"""
        if self.ended:
            raise RuntimeError("Called tick after the animation ended")
        if self._cur >= len(self.frames):
            if self.looped:
                self.restart()
                return True
            else:
                self.ended = True
                return False
        self._i += 1
        if self._i == self.timings[self._cur]:  # if the counter reached the value in the next position in the list
            self.image = self.frames[self._cur]  # set the new frame
            self._cur += 1  # begin waiting for the next frame
            return True  # indicate the change NOTE: For the time being, will be removed
        else:
            return False  # indicate no change


class RotatingAnim:
    """Animation that rotates the sprite"""
    def __init__(self, image, d_alpha, to_alpha=360, *args):
        """args include: 'loop', 'reverse', ... (WIP)"""
        self.image = image  # current image, begin with the first frame
        self._base_image = image
        self.rect = self.image.get_rect()
        self.d_alpha = d_alpha  # animation counter
        self.to_alpha = to_alpha
        self.alpha = 1  # animation frame (skip the first)
        self.looped = 'loop' in args  # detect if the animation is looped
        self.ended = False

    def restart(self):
        self.alpha = 0
        self.image = self._base_image
        self.ended = False

    def tick(self, *args):
        """Tick every frame"""
        if self.ended:
            raise RuntimeError("Called tick after the animation ended")
        if self.alpha >= self.to_alpha:
            if self.looped:
                self.restart()
                return True
            else:
                self.ended = True
                return False
        self.alpha += self.d_alpha
        print(self.alpha)
        self.image, self.rect = rot_center(self._base_image, self.rect, self.alpha)
        return True  # indicate the change NOTE: For the time being, will be removed
