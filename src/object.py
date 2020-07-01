from src.util import *


class Object:
    """Physics object"""

    def __init__(self, sprite, x, y, angle=0.0):
        """sprite is a tuple of pygame.sprite and pygame.rect, x,y are global spawn coordinates, angle clockwise"""
        self.x = x  # Global
        self.y = y  # Global
        self.angle = angle
        self.sprite = sprite[0]  # pygame.sprite
        self.rect = sprite[1]  # pygame.rect

    def tp(self, to_x, to_y, is_relative=False):  # global
        if is_relative:
            self.x += to_x
            self.y += to_y
        else:
            self.x = to_x
            self.y = to_y


class Entity(Object):
    """Has hp, armor, speed, max_hp, and sub-Object"""

    def __init__(self, sprite, x, y, max_hp, armor, speed, angle=0.0, hp=0):
        super().__init__(sprite, x, y, angle)
        self.max_hp = max_hp
        self.armor = armor
        self.speed = speed
        self.moving_u = False
        self.moving_r = False
        self.moving_d = False
        self.moving_l = False
        if hp:
            self.hp = hp
        else:
            self.hp = max_hp

    def kill(self):
        self.hp = 0

    def update(self):
        """Movement and AI"""
        if self.moving_u:
            self.rect.y -= self.speed
        if self.moving_d:
            self.rect.y += self.speed
        if self.moving_r:
            self.rect.x -= self.speed
        if self.moving_l:
            self.rect.x += self.speed
        # TODO: Better algorithm?


class GUI(Object):
    """Interface elements, no AI"""

    def __init__(self, sprite, x, y, on_click_action, on_hover_action, angle=0.0):
        """x,y, are relative (screen), on_click and on_hover actions must be function objects"""
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


class View:
    """Handling the contents of the screen"""

    def __init__(self, player, screen):
        self.player = player
        self.screen = screen
        self.x = player.x
        self.y = player.y
        self.rect = screen.get_rect()

    def update(self):
        self.x = self.player.x  # The screen must always follow the player
        self.y = self.player.y  # Placeholder for an algorithm
