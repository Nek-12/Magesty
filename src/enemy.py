from src.object import *


class Crawler(Entity):
    """The most basic evil dude, melee attack, simple ai"""
    def __init__(self, spritepack, hitsoundpack, target, x, y, max_hp, armor, speed, angle=0.0, hp=0):
        self.spritepack = spritepack
        super().__init__(spritepack['idle'], x, y, max_hp, armor, speed, angle, hp)
        self.target = target
        self.hitsoundpack = hitsoundpack
        self.stunned_for = 120

    def kill(self):
        self._die()
        super().kill()

    def _die(self):
        super()._die()
        self.hitsoundpack.play_random()

    def ai(self):
        if not self.rect.colliderect(self.target.rect):
            # TODO: Omg what a bullshit
            if self.target.x < self.x:  # target is to the left
                self.moving_l = True
                self.moving_r = False
            else:
                self.moving_r = True
                self.moving_l = False
            if self.target.y < self.y:  # target is above
                self.moving_u = True
                self.moving_d = False
            else:
                self.moving_d = True
                self.moving_u = False
        else:
            self.target.hit(10)
            self.stun(120)

    def update(self):
        super().update()
        if self.blocked:
            self.image = self.spritepack['attack']
            # TODO: No way to see the idle sprite, add attributes
        elif self.moving_u:
            self.image = self.spritepack['up']
        elif self.moving_d:
            self.image = self.spritepack['down']
        self.ai()

    def blit(self, screen):
        super().blit(screen)