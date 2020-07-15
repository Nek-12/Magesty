from src.object import *


class Orb(Object):
    """A cool colorful orb that rotates around the player every frame"""
    OFFSET = 50

    def __init__(self, color: str, x_offset, y_offset, owner: Entity = None, speed=15):
        """color can be: 'green', 'blue','yellow' offsets are from the owner's center"""
        self.color = color
        if color == 'green':
            self.anim = data.Anims.green_orb
            self.fly_anim = data.Anims.green_orb_fly
        elif color == 'blue':
            self.anim = data.Anims.blue_orb
            self.fly_anim = data.Anims.blue_orb_fly
        elif color == 'yellow':
            self.anim = data.Anims.yellow_orb
            self.fly_anim = data.Anims.yellow_orb_fly
        else:
            raise ValueError(f"This type of orb doesn't exist: {color}")
        self.sound_release = data.SFX.orb_release
        self.sound_release.play()
        self.sound_explode = data.SFX.orb_explode
        self.explosion_anim = data.Anims.small_explosion
        self.owner = owner
        self.distance = 0.0
        self.speed = speed
        self.damage = 10  # TODO: TEMP
        self.free = self.owner is None
        self.exploded = False
        self._dalpha = 0.05
        self.timer = 1000 * data.FRAMES_PER_MS  # lives for 2 seconds
        super().__init__(self.anim.base_image, self.owner.rect.centerx + x_offset, self.owner.rect.centery + y_offset)

    def release(self, angle):
        self.anim = self.fly_anim
        self.anim.restart(self)
        self.angle = angle
        self.free = True
        self.sound_release.play()

    def explode(self):
        self.angle = 0
        self.owner = None
        self.exploded = True
        self.anim = self.explosion_anim
        self.anim.restart(self)
        self.sound_explode.play()
        self.rect = pg.rect.Rect(self.x, self.y, 100, 100)
        for o in self.collision_test(data.entities):
            o.hit(self.damage)
            o.stun(self.damage * 100)  # TODO: Temp

    def update(self):
        super().update()
        if self.exploded:
            pass
        elif self.free:
            self.timer -= 1
            if not self.timer:
                self.explode()
            for obj in self.collision_test(data.entities):
                if obj is not self.owner:  # ignore the owner
                    self.explode()
                    return  # stop everything
            self.x += math.cos(self.angle) * self.speed  # fly
            self.y += math.sin(self.angle) * self.speed
        else:
            if self.distance < self.OFFSET:
                self.distance += self.OFFSET / 50
            ocx = self.owner.rect.centerx
            ocy = self.owner.rect.centery
            self.x = ocx + self.distance
            self.y = ocy + self.distance
            self.angle += self._dalpha
            rotated_x = (math.cos(self.angle) * (self.x - ocx) -
                         math.sin(self.angle) * (self.y - ocy) + ocx)
            rotated_y = (math.sin(self.angle) * (self.x - ocx) +
                         math.cos(self.angle) * (self.y - ocy) + ocy)
            self.x, self.y = rotated_x, rotated_y  # Rotate the orb around the owner's center
        if self.anim.ended:  # the only NOT looped animation is explosion animation
            self.kill()  # so we die if we stopped exploding
            return
        self.anim.tick(self)

    def blit(self, screen):
        super().blit(screen)

    def kill(self):
        super().kill()


class Player(Entity):
    def __init__(self, x, y, ai: AI, items: list, max_hp, speed=0, armor=0):
        """This function uses the values in data.py"""
        self.move_anims = data.Anims.player_move
        self.items = items
        self.anim = None
        self.idle_image = data.player_idle_image
        self.max_orbs = 3
        super().__init__(self.idle_image, x, y, ai, max_hp, armor, speed)
        self.orbs = []

    def _distribute_orbs(self):
        orbcnt = len(self.orbs)
        if orbcnt > 1:
            dalpha = 2 * math.pi / orbcnt  # 360 degrees split into equal parts
            i = 0
            for orb in self.orbs:
                i += 1
                orb.angle = dalpha * i
                orb.distance = 0
            # teleport orbs to new coords

    def add_orb(self, color):
        if len(self.orbs) < self.max_orbs:
            orb = Orb(color, 0, 0, self)
            self.orbs.append(orb)  # add the orb
            self._distribute_orbs()  # get them into the right positions

    def pop_orb(self):
        """Explodes an orb immediately"""
        if self.orbs:
            orb = self.orbs.pop()
            self._distribute_orbs()
            orb.add(data.objects)
            orb.explode()
            return orb
        return None

    def release_orb(self, angle):
        """Sends the orb flying in the direction, angle in RADIANS"""
        if self.orbs:
            orb = self.orbs.pop()
            orb.release(angle)  # orb begins to fly
            orb.add(data.objects)  # Orb adds itself to objects, becoming independent
            return orb
        return None

    def update(self):
        super().update()
        if not self.stunned():
            direction = self.ai.get_direction()
            if direction:
                self.anim = self.move_anims[direction]
                self.anim.tick(self)
            else:

                self.image = self.idle_image
        for orb in self.orbs:
            orb.update()

    def blit(self, screen):
        super().blit(screen)
        for orb in self.orbs:
            orb.blit(screen)

    def attack(self, target):
        super().attack(target)
