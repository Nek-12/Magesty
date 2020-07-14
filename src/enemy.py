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
            self.angle = math.atan2((self.target.y - self.y), (self.target.x - self.x))
            self.x += self.speed * math.cos(self.angle)
            self.y += self.speed * math.sin(self.angle)
        else:
            self.target.hit(10)
            self.stun(1000)

    def update(self):
        super().update()
        if self.blocked:
            self.image = self.spritepack['attack']
            # TODO: No way to see the sprites
        elif self.moving_u:
            self.image = self.spritepack['up']
        elif self.moving_d:
            self.image = self.spritepack['down']
        self.ai()

    def blit(self, screen):
        super().blit(screen)
