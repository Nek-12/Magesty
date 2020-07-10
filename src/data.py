from src.util import *
# import json
from src.misc import *

# TODO: Since the player is never killed, remove redundant entries and move them to constructor arguments,
#  remove dependency on the data class, remove garbage attributes

class Data:
    def __init__(self, game, fname):
        self.volume = 0.0
        self.game = game
        self.fps = 60
        self.player_max_hp = 100
        self.slash_sounds = load_soundlist('swing')
        self.meat_sounds = load_soundlist('meat')
        self.music = load_sound('music.wav')
        self.player_move_anims = load_animations_dictionary('char_move', (0, 0, 32, 32), 4, -1, 'loop')
        for a in self.player_move_anims.values():  # for every SpriteAnim object
            a.frames, a.rects = upscale_anim(a.frames, 4.0)
        self.player_sprite = self.player_move_anims['d'].frames[0]
        self.player_attack_anims = load_animations_dictionary('char_attack', (0,0,32,32), 4, -1, 'loop')
        for a in self.player_attack_anims.values():
            a.frames, a.rects = upscale_anim(a.frames, 4.0)
        self.player_defence = 1
        self.player_speed = 15
        self.slash_anim = load_anim('slash_1', -1)  # a tuple of frames and timings
        self.slash_anim = (upscale_anim(self.slash_anim[0], 2)[0], self.slash_anim[1])
        self.keydown_actions = None
        self.keyup_actions = None
        self.crawler_spritepack = load_sprite_dictionary('crawler', -1)
        for el in self.crawler_spritepack.values():  # for every image
            el = upscale_image(el[0], 4)[0]  # get rid of rects, leave frames
        # TODO: Introduce uniform behavior for these things

    def save(self):
        pass

    def load(self, game):
        self.keydown_actions = {
            pg.K_F11: toggle_fullscreen,
            pg.K_F12: pg.quit,
            pg.K_w: lambda: setattr(game.player, 'moving_u', True),
            pg.K_a: lambda: setattr(game.player, 'moving_l', True),
            pg.K_s: lambda: setattr(game.player, 'moving_d', True),
            pg.K_d: lambda: setattr(game.player, 'moving_r', True),
            pg.K_SPACE: getattr(game.player, 'slash')  # gets a callable class object reference
        }
        # P.S. We can't use assignment in lambdas
        self.keyup_actions = {
            pg.K_w: lambda: setattr(game.player, 'moving_u', False),
            pg.K_a: lambda: setattr(game.player, 'moving_l', False),
            pg.K_s: lambda: setattr(game.player, 'moving_d', False),
            pg.K_d: lambda: setattr(game.player, 'moving_r', False),
        }
