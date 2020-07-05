from src.util import *


class Animation(pg.sprite.Sprite):
    """A class that conveniently switches frames by a call."""

    def __init__(self, anim_tuple, *args):
        """args include: 'loop', 'reverse', 'rotation'... (WIP)"""
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
        self.slash = Slash(self, data.slash_anim, data.slash_sound)  # Create an attack

    def update(self):
        super().update()
        self.rect.x, self.rect.y = self.x, self.y
        # Note: WIP

    def blit(self):
        self.slash.blit(self.game.screen)  # draw the slash first
        self.game.screen.blit(self.image, self.rect)  # draw self over the slash


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
        if self.sound:
            self.sound.play()  # play the sound at the animation start
        self.slashing = True
        self.anim.restart()

    def blit(self, screen):  # Every time we blit
        if self.slashing:  # If slashing
            self.rect.center = self.owner.rect.center  # Follow the player
            if self.anim.tick():  # if the animation changed
                self.image = self.anim.image  # assign the new frame
            elif self.anim.ended:  # but if we stopped
                self.slashing = False
            screen.blit(self.image, self.rect)
