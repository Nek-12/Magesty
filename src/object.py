from src.util import *


class Object(pg.sprite.Sprite):  # derive from Sprite to get the image and rectangle
    """Physics object"""

    def __init__(self, sprite, x, y, angle=0.0):
        """sprite is a tuple of pygame.sprite and pygame.rect, x,y are global spawn coordinates, angle clockwise"""
        super().__init__()
        self.x = x  # Global
        self.y = y  # Global
        self.angle = angle
        self.sprite = sprite[0]  # pygame.sprite
        self.rect = sprite[1]  # pygame.rect
        # TODO: Figure out the attributes the Sprite class has and don't duplicate them.

    def tp(self, to_x, to_y, is_relative=False):  # global
        if is_relative:
            self.x += to_x
            self.y += to_y
        else:
            self.x = to_x
            self.y = to_y

    def update(self, *args): # super().update does nothing but can be called on Groups
        pass

    def kill(self):
        # Whatever
        super().kill()  # Remove this object from ALL Groups it belongs to.


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
        self.hp = 0  # Kill the entity

        super().kill()  # Kill the object

    def update(self):  # overrides the Object.update() method
        """Movement and AI"""
        super().update()  # Call the Object update method
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
    def __init__(self, sprite, x, y, max_hp, defence, speed, res):
        super().__init__(sprite, x, y, max_hp, defence, speed)
        self.rect.x = res[0] // 2 - sprite[0].get_width() // 2
        self.rect.y = res[1] // 2 - sprite[0].get_height() // 2
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
        self.half_player_size = self.player.sprite.get_width() // 2, self.player.sprite.get_height() // 2

    @staticmethod
    def update(screen_size, mouse_pos, player_pos):
        # TODO: make camera movement smoother
        dx = mouse_pos[0] - screen_size[0] // 2
        expected_x = screen_size[0] // 2 - dx // 2
        if expected_x - player_pos[0] > 0:
            if expected_x - player_pos[0] > 10:
                x = player_pos[0] + 10
            else:
                x = expected_x
        else:
            if expected_x - player_pos[0] < -10:
                x = player_pos[0] - 10
            else:
                x = expected_x

        dy = mouse_pos[1] - screen_size[1] // 2
        expected_y = screen_size[1] // 2 - dy // 2
        if expected_y - player_pos[1] > 0:
            if expected_y - player_pos[1] > 10:
                y = player_pos[1] + 10
            else:
                y = expected_y
        else:
            if expected_y - player_pos[1] < -10:
                y = player_pos[1] - 10
            else:
                y = expected_y
        return x, y
