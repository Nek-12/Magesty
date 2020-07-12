from src.util import *
from abc import ABCMeta, abstractmethod


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

    def upscale_frames(self, coefficient):
        self.frames = upscale_anim(self.frames, coefficient)
        self.base_image = self.frames[0]

    def set_frames(self, frames_list, are_reversed=False):
        if are_reversed:
            self.frames = reversed(frames_list)
        else:
            self.frames = frames_list  # images
        self.base_image = self.frames[0]
        self.rect = self.base_image.get_rect

    def restart(self, owner):
        super().restart(owner)
        self._i = 0
        self._cur = 1
        owner.image = self.base_image  # sets the frame to first
        # self.owner.rect = self.rects[0]  # sets the rect

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
        mul = -1*('reversed' in tags)
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

