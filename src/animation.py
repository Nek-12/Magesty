from src.util import *
# TODO: Make methods pure virtual


class Animation:
    """A class that conveniently switches frames by a call.
    Usage: call self.animation.tick() every frame -> frame changes if necessary"""
    def __init__(self, owner):
        self.owner = owner
        self.ended = owner is None  # If there is no owner, you can't animate!

    def tick(self):
        if self.ended:
            raise RuntimeError(f"Called tick after the animation ended, owner: {self.owner}")

    def restart(self):
        self.ended = self.owner is None


class SpriteAnim(Animation):
    def __init__(self, owner, anim_and_timings, *args):
        """anim_and_timings=(frames list, timings list), args include: 'loop', 'reverse'
        if reversed, the timings still must be supplied correctly"""
        super().__init__(owner)
        if 'reverse' in args:
            self.frames = reversed(anim_and_timings[0])
        else:
            self.frames = anim_and_timings[0]  # images
        self.looped = 'loop' in args  # detect if the animation is looped
        self.owner = owner
        if self.owner:
            self.owner.image = self.frames[0]  # set the image
        self.timings = anim_and_timings[1]
        self.rects = [r.get_rect() for r in self.frames]
        self._i = 0  # animation counter
        self._cur = 0  # animation frame (skip the first)

    def restart(self):
        super().restart()
        self._i = 0
        self._cur = 1
        self.owner.image = self.frames[0]  # sets the frame to first
        # self.owner.rect = self.rects[0]  # sets the rect

    def tick(self):
        """Call tick every frame"""
        super().tick()
        if self._cur >= len(self.frames):
            if self.looped:
                self.restart()
                return True
            else:
                self.ended = True
                return False
        self._i += 1
        if self._i == self.timings[self._cur]:  # if the counter reached the value in the next position in the list
            self._i = 0
            self.owner.image = self.frames[self._cur]  # set the new frame
            self._cur += 1  # begin waiting for the next frame
            return True  # changed
        else:
            return False  # indicate no change


class RotatingAnim(Animation):
    """Animation that rotates the sprite"""
    # TODO: Add speedup/slowdown

    def __init__(self, owner, image, d_alpha, to_alpha=360, *args):
        """args include: 'loop', 'reverse'"""
        super().__init__(owner)
        self.owner.image = image
        self._base_image = image
        self.rect = image.get_rect()
        mul = -1*('reversed' in args)
        self.d_alpha = d_alpha * mul  # animation counter
        self.to_alpha = to_alpha * mul
        self.alpha = 0
        self.looped = 'loop' in args  # detect if the animation is looped

    def restart(self):
        super().restart()
        self.alpha = 0
        self.owner.image = self._base_image


    def tick(self):
        """Tick every frame"""
        super().tick()
        if self.alpha >= self.to_alpha:
            if self.looped:
                self.restart()
                return True
            else:
                self.ended = True
                return False
        self.alpha += self.d_alpha
        print(self.alpha)
        self.owner.image, self.owner.rect = rot_center(self._base_image, self._base_image.get_rect(), self.alpha)
        # TODO: Test collision handling
        return True  # indicate the change


class BlinkingAnim(Animation):
    """Blinks with the specified parameters"""
    def __init__(self, owner, image, d_alpha, times=0, starting_alpha=0):
        """If times = 0, then the animation works indefinitely"""
        super().__init__(owner)
        self.image = image
        self.d_alpha = d_alpha
        self.times = times
        self._base_alpha = starting_alpha
        self.alpha = starting_alpha
        self._i = 0

    def restart(self):
        self.alpha = self._base_alpha
        self.owner.image
