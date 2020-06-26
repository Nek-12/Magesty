from src.util import *

class Object:
    """Any object in the game"""

    def __init__(self, sprite, x, y, angle=0.0):
        self.x = x
        self.y = y
        self.angle = angle
        self.sprite = sprite[0]
        self.rect = sprite[1]

    def tp(self, to_x, to_y, is_relative=False):
        if is_relative:
            self.x += to_x
            self.y += to_y
        else:
            self.x = to_x
            self.y = to_y


class Entity(Object):
    """Alive object:"""

    def __init__(self, sprite, x, y, max_hp, armor, speed, angle=0.0, hp=0):
        super().__init__(sprite, x, y, angle)
        self.max_hp = max_hp
        self.armor = armor
        self.speed = speed
        if hp:
            self.hp = hp
        else:
            self.hp = max_hp

    def kill(self):
        self.hp = 0

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

class GUI(Object):
    """Interface elements"""

    def __init__(self, sprite, x, y, on_click_action, on_hover_action, angle=0.0):
        super().__init__(sprite, x, y, angle)
        self.on_click_action = on_click_action
        self.on_hover_action = on_hover_action


class Player(Entity):
    def __init__(self, sprite, x, y, max_hp, defence, speed):
        super().__init__(sprite, x, y, max_hp, defence, speed)
        self.rect.x = x
        self.rect.x = y
        # TODO: remove usage of screen coords

    def update(self):
        super().update()

