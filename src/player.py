from src.object import *


class Orb(Object):
    """A cool colorful orb that rotates around the player every frame"""
    OFFSET = 50

    def __init__(self, owner: Entity, color: str, x_offset, y_offset, angle_per_frame=0.05, ):
        """color can be: 'green', 'blue','yellow' offsets are from the owner's center"""
        self.color = color
        if color == 'green':
            self.anim = data.green_orb_anim
        elif color == 'blue':
            self.anim = data.blue_orb_anim
        elif color == 'yellow':
            self.anim = data.yellow_orb_anim
        else:
            raise ValueError(f"This type of orb doesn't exist: {color}")
        self.soundpack = None
        self.owner = owner
        self.distance = 0.0
        self._dalpha = angle_per_frame  # RADIANS
        super().__init__(self.anim.base_image, self.owner.rect.centerx+x_offset, self.owner.rect.centery+y_offset)

    def to_rel_pos(self, x_offset, y_offset):
        self.x = x_offset + self.owner.rect.centerx
        self.y = y_offset + self.owner.rect.centery

    def update(self):
        super().update()
        if self.distance < self.OFFSET:
            self.distance += self.OFFSET/50
        ocx = self.owner.rect.centerx
        ocy = self.owner.rect.centery
        self.x = ocx+self.distance
        self.y = ocy+self.distance
        self.angle += self._dalpha
        rotated_x = (math.cos(self.angle) * (self.x - ocx) -
                     math.sin(self.angle) * (self.y - ocy) + ocx)
        rotated_y = (math.sin(self.angle) * (self.x - ocx) +
                     math.cos(self.angle) * (self.y - ocy) + ocy)
        self.x, self.y = rotated_x, rotated_y  # Rotate the orb around the owner's center
        self.anim.tick(self)

    def blit(self, screen):
        super().blit(screen)


class Player(Entity):
    def __init__(self):
        """This function uses the values in data.py"""
        self.move_anims = data.player_move_anims
        self.anim = self.move_anims['d']
        self.idle_image = data.player_idle_image
        super().__init__(data.player_idle_image, 0, 0, data.player_max_hp, data.player_defence, data.player_speed)
        self.orbs = []

    def _distribute_orbs(self):
        orbcnt = len(self.orbs)
        if orbcnt > 1:
            dalpha = 2 * math.pi / orbcnt  # 360 degrees split into equal parts
            for i in range(orbcnt):
                self.orbs[i].angle = dalpha*i
                self.orbs[i].distance = 0
            # teleport orbs to new coords

    def add_orb(self, color: str):
        self.orbs.append(Orb(self, color, 0, 0))  # add the orb
        self._distribute_orbs()  # get them into the right positions

    def del_orb(self, color=None):
        if color:
            for i in range(len(self.orbs)):
                if self.orbs[i].color == color:
                    self.orbs.pop(i)
                    break
        else:
            if self.orbs:
                self.orbs.pop()
        self._distribute_orbs()

    def _select_anim(self):
        s = ''
        if self.moving_u:
            s = 'u'
        elif self.moving_d:
            s = 'd'
        elif self.moving_l:
            s = 'l'
        elif self.moving_r:
            s = 'r'
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
