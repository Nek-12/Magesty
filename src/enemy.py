from src.object import *
from src.sound import SoundPack
from src.player import Player
from random import choice


class Crawler(Entity):
    """The most basic evil dude, melee attack, simple ai"""

    def __init__(self, spritepack: dict,
                 hitsoundpack: SoundPack,
                 target: Entity,
                 x, y, max_hp, armor, speed, hp=0):
        self.spritepack = spritepack
        self.target = target
        super().__init__(spritepack['idle'], x, y, ChasingTargetMeleeAI(self, target), max_hp, armor, speed, hp)
        self.hitsoundpack = hitsoundpack
        self.stun(500)
        self.bash_duration_ms = 150
        self.attack_cooldown = 1000
        self.self_attack_stun = 1000
        self.damage = 10

    def hit(self, hp):
        self.hitsoundpack.play_random()
        self.stun(200)
        super().hit(hp)

    def kill(self):
        self.hp = 0
        super().kill()

    def update(self):
        super().update()
        d = self.ai.get_direction()
        if self.stunned():
            self.image = self.spritepack['attack']
        elif d:
            self.image = self.spritepack[d]
        else:
            self.image = self.spritepack['idle']

    def blit(self, screen):
        super().blit(screen)


class Wizard(Player):  # Yes this wizard is basically another player
    """The basic wizard who can shoot fireballs at player"""

    def __init__(self, x, y, target, reload_ms, max_hp: int, speed: int, shooting_range: int,
                 armor=0):  # TODO: Add spritepack and soundpack to params, not const, messy!
        self.shoot_range = shooting_range
        self.stun(500)
        super().__init__(x, y, ChasingTargetRangedAI(self, target, reload_ms), [], max_hp, speed, armor)
        self.move_anims = data.Anims.wizard_move
        self.anim = None
        self.idle_image = data.wizard_idle_image
        self.cooldown = 120  # TODO: Temporary
        self._i = 0

    def update(self):
        super().update()
        if self._i:
            self._i -= 1  # try to reload
        else:
            self._i = self.cooldown
            self.add_orb(choice(('green', 'yellow', 'blue')))

    def blit(self, screen):
        super().blit(screen)

    def attack(self, target):
        if self.orbs:
            self.release_orb(angle_to(self, target))
