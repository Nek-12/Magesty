from src.object import *
import math

class Crawler(Entity):
    """The most basic evil dude, melee attack, simple ai"""
    def __init__(self, spritepack, hitsoundpack, target, x, y, max_hp, armor, speed, hp=0):
        self.spritepack = spritepack
        super().__init__(spritepack['idle'], x, y, max_hp, armor, speed, hp)
        self.target = target
        self.hitsoundpack = hitsoundpack
        self.stunned_for = 500

    def hit(self, hp):
        self.hitsoundpack.play_random()
        self.stun(200)
        super().hit(hp)

    def kill(self):
        self.hp = 0
        super().kill()

    def ai(self):
        self.stop()
        if not self.rect.colliderect(self.target.rect):
            # TODO: Omg what a bullshit
            if self.target.x < self.x:  # target is to the left
                self.moving_l = True
            elif self.target.x > self.x:
                self.moving_r = True
            if self.target.y < self.y:  # target is above
                self.moving_u = True
            elif self.target.y > self.y:
                self.moving_d = True
        else:
            self.target.hit(10)
            self.stun(1000)

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
