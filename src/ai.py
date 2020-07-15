import pygame as pg
from abc import ABCMeta, abstractmethod
from src.util import distance
from src.data import FRAMES_PER_MS


class AI(metaclass=ABCMeta):
    def __init__(self, owner, target=None):
        self.owner = owner
        self.target = target
        self._norm_v = pg.Vector2()  # normalized direction vector

    def get_direction(self) -> str:
        ret = ''
        if self._norm_v.y < 0:
            ret = 'u'  # REVERSED because of the reversed y axis (screen)
        elif self._norm_v.y > 0:
            ret = 'd'
        elif self._norm_v.x < 0:
            ret = 'l'
        elif self._norm_v.x > 0:
            ret = 'r'
        return ret

    def chase_target(self):
        self._norm_v = pg.Vector2((self.target.x - self.owner.x), (self.target.y - self.owner.y)).normalize()
        self.owner.x += self.owner.speed * self._norm_v.x
        self.owner.y += self.owner.speed * self._norm_v.y

    @abstractmethod
    def update(self, *args):
        pass

    def move(self, direction: str):
        pass

    def stop(self, direction: str = None):
        if direction is None:
            self._norm_v = pg.Vector2()


class KeybordControllableAI(AI):
    """An AI that handles keyboard input"""
    DIRECTIONS = {
        'up': (0, -1),
        'down': (0, 1),
        'left': (-1, 0),
        'right': (1, 0),
    }

    def __init__(self, owner):
        super().__init__(owner)

    def move(self, direction: str):
        self._norm_v += pg.Vector2(self.DIRECTIONS[direction])  # rotate the vector

    def stop(self, direction: str = None):
        if direction is None:
            super().stop()
        else:
            self._norm_v -= pg.Vector2(self.DIRECTIONS[direction])  # subtract the reversed direction

    def update(self):
        self.owner.x += self.owner.speed * self._norm_v.x
        self.owner.y += self.owner.speed * self._norm_v.y


# TODO: Broken

class ChasingTargetMeleeAI(AI):
    def __init__(self, owner, target):
        super().__init__(owner, target)

    def update(self):
        if not self.owner.rect.colliderect(self.target.rect):
            self.chase_target()
        else:
            self.owner.attack(self.target)
        super().update()


class ChasingTargetRangedAI(AI):
    def __init__(self, owner, target, reload_ms):
        super().__init__(owner)
        assert self.owner.shoot_range > 100, f"Range is {self.owner.shoot_range}"
        self.target = target
        self.reload_time = reload_ms * FRAMES_PER_MS
        self._i = self.reload_time

    def update(self):
        self._i -= 1
        if distance(self.owner, self.target) > self.owner.shoot_range:
            self.chase_target()
        elif self._i > 0:
            self.stop()
        else:
            self.owner.attack(self.target)
            self._i = self.reload_time
        super().update()

