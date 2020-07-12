from src.util import *
import src.data as data
from src.object import *

class Spell(Object):
    def __init__(self, owner, animation, soundpack, damage: int, power: int, orbs: list[Orb]):
        """Owner is the entity who cast the spell"""
        self.anim = animation  # Load an animation
        self.damage = damage
        self.power = power
        self.orbs = orbs
        super().__init__(animation.base_image, owner.x, owner.y)  # first frame
        self.owner = owner  # store the reference
        self.soundpack = soundpack

    def __call__(self, targets):  # If the object is called
        pass

    def update(self, *args):
        self.anim.tick(self)

    def blit(self, screen):
        super().blit(screen)


class Slash(Spell):
    """Lightning strike"""

    def __init__(self, owner: Entity, damage: int, power: int, orbs: list[Orb]):
        super().__init__(owner, data.slash_anim, data.swing_soundpack, damage, power, orbs)

    def __call__(self, targets):  # If the object is called
        pass

    def update(self):  # Every time we blit
        super().blit(data.screen)
