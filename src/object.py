import src.data as data
import math
from src.ai import *
from src.util import *


class Object(pg.sprite.Sprite):  # derive from Sprite to get the image and rectangle
    """Physics object"""

    def __init__(self, image, x, y):
        """x,y are global spawn coordinates"""
        super().__init__()
        self.x = x  # Global
        self.y = y  # Global
        self.image = image  # pygame.sprite.image
        self.rect = image.get_rect()  # pygame.sprite.rect
        self.angle = 0  # RADIANS

    def tp(self, to_x, to_y, is_relative=False):  # global
        if is_relative:
            self.x += to_x
            self.y += to_y
        else:
            self.x = to_x
            self.y = to_y

    def rotate(self, angle=0):
        """rotates the image of the object and sets it angle (degrees) to the value
        If you don't supply an angle, the image will be rotated according to the internal angle"""
        self.image, self.rect = rot_center(self.image, self.rect, self.angle)

    def update(self):  # super().update does nothing but can be called on Groups
        super().update()
        self.rect.centerx = self.x
        self.rect.centery = self.y  # TEMPORARY

    def blit(self, screen):
        screen.blit(self.image, self.rect)  # draw self

    def kill(self):
        # Whatever
        super().kill()  # Remove this object from ALL Groups it belongs to.

    def collision_test(self, targets: list):
        """Test collistion of obj and all the targets (list)"""
        collided_objects = []
        for o in targets:
            if o.rect.colliderect(self):
                collided_objects.append(o)
        return collided_objects


class Entity(Object):
    """Has hp, armor, speed, max_hp, and sub-Object"""

    def __init__(self, sprite, x, y, ai: AI, max_hp, armor, speed, hp=0):
        super().__init__(sprite, x, y)
        self.ai = ai
        self.max_hp = max_hp
        self.armor = armor
        self.speed = speed
        self.bash_duration_ms = 0
        self.self_attack_stun = 0
        self._stunned_for = 0.0  # FRAMES
        self.damage = 10  # TODO: Temporary
        if hp:
            self.hp = hp
        else:
            self.hp = max_hp

    def stun(self, ms):
        """Stun the Entity (make it idle)"""
        self._stunned_for = data.to_frames(ms)  # convert to frames

    def stunned(self):
        return self._stunned_for > 0 or self._stunned_for == -1

    def hit(self, hp):
        self.hp -= hp
        if self.hp < 0:
            super().kill()  # Kill the object

    def update(self):  # overrides the Object.update() method
        """Movement and AI"""
        super().update()  # Call the Object update method
        if self._stunned_for > 0:
            self._stunned_for -= 1  # subtract one frame
        elif self._stunned_for == -1:
            pass
        else:
            self.ai.update()  # if not stunned, allow the ai to work

    def attack(self, target):
        target.hit(self.damage)
        target.stun(self.bash_duration_ms)
        self.stun(self.self_attack_stun)  # to allow the target to escape

# class GUI(Object):
#     """Interface elements, no AI"""
#
#     def __init__(self, sprite, x, y, on_click_action, on_hover_action, angle=0.0):
#         """x,y, are relative (screen), on_click and on_hover actions must be function objects"""
#         super().__init__(sprite, x, y)
#         self.on_click_action = on_click_action
#         self.on_hover_action = on_hover_action
