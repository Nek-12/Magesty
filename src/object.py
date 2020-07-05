from src.util import *
from src.misc import *


class Object(pg.sprite.Sprite):  # derive from Sprite to get the image and rectangle
    """Physics object"""

    # TODO: Replace naked pg.sprites with Animations and avoid duplicates
    def __init__(self, image, x, y, angle=0.0):
        """x,y are global spawn coordinates, angle clockwise"""
        super().__init__()
        self.x = x  # Global
        self.y = y  # Global
        self.angle = angle
        self.image = image  # pygame.sprite.image
        self.rect = image.get_rect()  # pygame.sprite.rect

    def tp(self, to_x, to_y, is_relative=False):  # global
        if is_relative:
            self.x += to_x
            self.y += to_y
        else:
            self.x = to_x
            self.y = to_y

    def update(self, *args):  # super().update does nothing but can be called on Groups
        if self.angle:
            self.image, self.rect = rot_center(self.image, self.rect, self.angle)  # Rotate
            self.angle = 0  # Stop rotating

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
            self.y -= self.speed
        if self.moving_d:
            self.y += self.speed
        if self.moving_r:
            self.x -= self.speed
        if self.moving_l:
            self.x += self.speed


class GUI(Object):
    """Interface elements, no AI"""

    def __init__(self, sprite, x, y, on_click_action, on_hover_action, angle=0.0):
        """x,y, are relative (screen), on_click and on_hover actions must be function objects"""
        super().__init__(sprite, x, y, angle)
        self.on_click_action = on_click_action
        self.on_hover_action = on_hover_action


class Player(Entity):
    def __init__(self, game):
        self.game = game
        data = self.game.data
        super().__init__(data.player_image, 0, 0, data.player_max_hp, data.player_defence, data.player_speed)
        self.attack = Slash(self, data.slash_anim, data.slash_sound)  # Create an attack
        self.attack_sprite = data.player_attacking_sprite

    def update(self):
        super().update()
        self.rect.x, self.rect.y = self.x, self.y
        if self.attack.slashing:
            self.image = self.attack_sprite
        else:
            self.image = self.game.data.player_image

    def blit(self):
        self.game.screen.blit(self.image, self.rect)  # draw self
        self.attack.blit(self.game.screen)  # draw the slash over self

    def slash(self):
        self.attack()


class Slash(Object):
    """Creates an attack for the entity"""

    def __init__(self, owner, anim_tuple, sound=None):
        """Owner is the Entity doing a slash, anim_tuple is returned by load_anim"""
        self.anim = Animation(anim_tuple)  # Load an animation
        super().__init__(self.anim.image, owner.x, owner.y)  # first frame
        self.owner = owner  # store the reference
        self.sound = sound
        self.angle = 0
        self.slashing = False

    def __call__(self):  # If the object is called
        if not self.slashing:
            if self.sound:
                self.sound.play()  # play the sound at the animation start
            self.slashing = True
            self.anim.restart()

    def blit(self, screen):  # Every time we blit
        if self.slashing:  # If slashing
            self.rect.center = self.owner.rect.center  # Follow the player
            if self.anim.tick():  # if the animation changed
                self.image = self.anim.image  # assign the new frame
                self.rect = self.anim.rect  # temporary workaround
            elif self.anim.ended:  # but if we stopped
                self.slashing = False
            screen.blit(self.image, self.rect)
