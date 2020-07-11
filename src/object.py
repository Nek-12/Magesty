from src.misc import *
from src.animation import *
from src.data import Data


class Object(pg.sprite.Sprite):  # derive from Sprite to get the image and rectangle
    """Physics object"""
    def __init__(self, image, x, y):
        """x,y are global spawn coordinates"""
        super().__init__()
        self.x = x  # Global
        self.y = y  # Global
        self.image = image  # pygame.sprite.image
        self.rect = image.get_rect()  # pygame.sprite.rect

    def tp(self, to_x, to_y, is_relative=False):  # global
        if is_relative:
            self.x += to_x
            self.y += to_y
        else:
            self.x = to_x
            self.y = to_y

    def rotate(self, angle):
        self.image, self.rect = rot_center(self.image, self.rect, angle)

    def update(self, *args):  # super().update does nothing but can be called on Groups
        super().update()
        self.rect.x = self.x
        self.rect.y = self.y  # TEMPORARY

    def blit(self, screen):
        screen.blit(self.image, self.rect)  # draw self

    def kill(self):
        # Whatever
        super().kill()  # Remove this object from ALL Groups it belongs to.


class Entity(Object):
    """Has hp, armor, speed, max_hp, and sub-Object"""
    def __init__(self, sprite, x, y, max_hp, armor, speed, hp=0):
        super().__init__(sprite, x, y)
        self.max_hp = max_hp
        self.armor = armor
        self.speed = speed
        self.moving_u = False
        self.moving_r = False
        self.moving_d = False
        self.moving_l = False
        self.blocked = False
        self.stunned_for = 0  # ms
        if hp:
            self.hp = hp
        else:
            self.hp = max_hp

    def stun(self, ms):
        """Stun the Entity (make it idle)"""
        self.blocked = True
        self.stunned_for = ms

    def stop(self):
        self.moving_u, self.moving_r, self.moving_d, self.moving_l = False, False, False, False

    def hit(self, hp):
        self.hp -= hp
        if self.hp < 0:
            super().kill()  # Kill the object

    def update(self):  # overrides the Object.update() method
        """Movement and AI"""
        super().update()  # Call the Object update method
        if not self.blocked:
            if self.moving_u:
                self.y -= self.speed
            if self.moving_d:
                self.y += self.speed
            if self.moving_r:
                self.x += self.speed
            if self.moving_l:
                self.x -= self.speed
        self.stunned_for -= 1000//Data.fps  # TODO: Use ms, not frames!
        if self.stunned_for < 0:
            self.blocked = False


# class GUI(Object):
#     """Interface elements, no AI"""
#
#     def __init__(self, sprite, x, y, on_click_action, on_hover_action, angle=0.0):
#         """x,y, are relative (screen), on_click and on_hover actions must be function objects"""
#         super().__init__(sprite, x, y)
#         self.on_click_action = on_click_action
#         self.on_hover_action = on_hover_action


class Player(Entity):
    def __init__(self, game):
        self.game = game
        data = self.game.data
        self.move_anims = data.player_move_anims
        self.attack_anims = data.player_attack_anims
        self.anim = self.move_anims['d']
        self.idle_image = data.player_sprite
        super().__init__(data.player_sprite, 0, 0, data.player_max_hp, data.player_defence, data.player_speed)
        self.rect.inflate_ip(-self.rect.width//2, -self.rect.height//2)
        self.anim.rect.inflate_ip(-self.rect.width // 2, -self.rect.height // 2)
        # TODO: Fix the rectangle problem, hitboxes are borked
        self.slash = Slash(self, data.slash_anim, data.slash_soundpack)  # Create an attack

    def _select_anim(self):
        s = ''
        if self.moving_u:
            s += 'u'
        elif self.moving_d:
            s += 'd'
        if self.moving_l:
            s += 'l'
        elif self.moving_r:
            s += 'r'
        return s

    # TODO: Inefficient algorithm, optimize

    def do_slash(self):
        self.slash(self.game.entities)

    def update(self):
        super().update()
        if self.slash.slashing:
            pass
            self.blocked = True
        else:
            self.blocked = False
            direction = self._select_anim()
            if direction:
                self.anim = self.move_anims[direction]
                self.anim.tick(self)
            else:
                self.image = self.idle_image
        self.slash.update()

    def blit(self, screen):
        super().blit(screen)
        self.slash.blit(screen)  # draw the slash over self


class Slash(Object):
    """Creates an attack for the entity"""

    def __init__(self, owner, anim_and_timings, sounds=None):
        """Owner is the Entity doing a slash, anim_and_timings is returned by load_anim"""
        self.anim = SpriteAnim(anim_and_timings)  # Load an animation
        super().__init__(anim_and_timings[0][0], owner.x, owner.y)  # first frame
        self.owner = owner  # store the reference
        self.sounds_miss = sounds
        self.slashing = False
        self.rect.inflate_ip(-self.rect.width//3, -self.rect.height//3)
        self.anim.rect.inflate_ip(-self.rect.width // 2, -self.rect.height // 2)

        # TODO: Why the hell the slash is always present? It should be created on call

    def __call__(self, targets):  # If the object is called
        if not self.slashing:
            if self.sounds_miss:
                self.sounds_miss.play_random()  # play the sound at the animation start
            self.slashing = True
            for i in collision_test(self, targets):
                i.hit(5)
            self.anim.restart(self)

    def update(self):  # Every time we blit
        if self.slashing:  # If slashing
            self.rect.center = self.owner.rect.center  # Follow the player
            self.anim.tick(self)  # advance the animation
            if self.anim.ended:  # but if we stopped
                self.slashing = False

    def blit(self, screen):
        if self.slashing:
            super().blit(screen)
