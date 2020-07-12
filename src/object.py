from src.misc import *
from src.animation import *
import src.data as data
import math


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

    def update(self):  # super().update does nothing but can be called on Groups
        super().update()
        self.rect.centerx = self.x
        self.rect.centery = self.y  # TEMPORARY

    def blit(self, screen):
        screen.blit(self.image, self.rect)  # draw self

    def kill(self):
        # Whatever
        super().kill()  # Remove this object from ALL Groups it belongs to.

    def collision_test(self, targets):
        """Test collistion of obj and all the targets (list)"""
        collided_objects = []
        for o in targets:
            if o.rect.colliderect(self):
                collided_objects.append(o)
        return collided_objects


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
        self.stunned_for -= data.MILLISECOND
        if self.stunned_for <= 0:
            self.blocked = False
            self.stunned_for = 0


class Orb(Object):
    """A cool colorful orb that rotates around the player every frame"""
    OFFSET = 1

    def __init__(self, owner: Entity, color: str, x_offset, y_offset, angle_per_frame=0.05, ):
        """type can be: 'green', 'blue','yellow' offsets are from the owner's center"""
        self.color = color
        if color == 'green':
            self.anim = data.green_orb_anim
        elif color == 'blue':
            self.anim = data.blue_orb_anim
        elif color == 'yellow':
            self.anim = data.yellow_orb_anim
        else:
            raise ValueError("This type of orb doesn't exits:"+color)
        self.soundpack = None
        self.owner = owner
        self.alpha = 0
        self._dalpha = angle_per_frame  # RADIANS
        super().__init__(self.anim.base_image, x_offset, y_offset)

    def to_rel_pos(self, x_offset, y_offset):
        self.rect.centerx = x_offset + self.owner.rect.centerx
        self.rect.centery = y_offset + self.owner.rect.centery

    def update(self):
        super().update()
        ocx = self.owner.rect.centerx
        ocy = self.owner.rect.centery
        self.x = ocx
        self.y = ocy
        rotated_x = (math.cos(self.alpha) * (self.x - ocx) -
                     math.sin(self.alpha) * (self.y - ocy) + ocx)
        rotated_y = (math.sin(self.alpha) * (self.x - ocx) +
                     math.cos(self.alpha) * (self.y - ocy) + ocy)
        # the rotation is RELATIVE to the current rotation
        self.alpha += self._dalpha
        self.x, self.y = rotated_x, rotated_y  # Rotate the orb around the owner's center
        self.anim.tick(self)


    def blit(self, screen):
        super().blit(screen)


# class GUI(Object):
#     """Interface elements, no AI"""
#
#     def __init__(self, sprite, x, y, on_click_action, on_hover_action, angle=0.0):
#         """x,y, are relative (screen), on_click and on_hover actions must be function objects"""
#         super().__init__(sprite, x, y)
#         self.on_click_action = on_click_action
#         self.on_hover_action = on_hover_action


class Player(Entity):
    def __init__(self):
        """This function uses the values in data.py"""
        self.move_anims = data.player_move_anims
        self.anim = self.move_anims['d']
        self.idle_image = data.player_idle_image
        super().__init__(data.player_idle_image, 0, 0, data.player_max_hp, data.player_defence, data.player_speed)
        self.rect.inflate_ip(-self.rect.width // 2, -self.rect.height // 2)
        self.anim.rect.inflate_ip(-self.rect.width // 2, -self.rect.height // 2)
        self.orbs = []

    def _distribute_orbs(self):
        orbcnt = len(self.orbs)
        dalpha = 2 * math.pi / orbcnt  # 360 degrees split into equal parts
        for i in range(orbcnt):
            self.orbs[i].to_rel_pos(x_offset=Orb.OFFSET * math.cos((i + 1) * dalpha),
                                    y_offset=Orb.OFFSET * math.sin((i + 1) * dalpha))
            # teleport orbs to new coords

    def add_orb(self, color: str):
        self.orbs.append(Orb(self, color, 0, 0))  # add the orb
        self._distribute_orbs()  # get them into the right positions

    def del_orb(self, color):
        for i in range(len(self.orbs)):
            if self.orbs[i].color == color:
                self.orbs.pop(i)
        self._distribute_orbs()

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

    def update(self):
        super().update()
        direction = self._select_anim()
        if direction:
            self.anim = self.move_anims[direction]
            self.anim.tick(self)
        else:
            self.image = self.idle_image
        if self.orbs:
            for orb in self.orbs:
                orb.update()

    def blit(self, screen):
        super().blit(screen)
        if self.orbs:
            for orb in self.orbs:
                orb.blit(screen)
