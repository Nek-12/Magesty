from src.util import *

class Data:

    def __init__(self, game, fname):
        self.game = game
        self.fps = 60
        self.player_max_hp = 100
        self.player_sprite = load_sprite("ninja.png")  # tuple
        self.player_defence = 1
        self.player_speed = 5
        self.keydown_actions = {
            pg.K_F11: toggle_fullscreen,
            pg.K_F12: sys.exit,
            pg.K_w: lambda: setattr(self.game.player, 'dy', -10),
            pg.K_a: lambda: setattr(self.game.player, 'dx', -10),
            pg.K_s: lambda: setattr(self.game.player, 'dy', 10),
            pg.K_d: lambda: setattr(self.game.player, 'dx', 10),
        }
        # P.S. We can't use assignment in lambdas
        self.keyup_actions = {
            pg.K_w: lambda: setattr(game.player, 'dy', 0),
            pg.K_a: lambda: setattr(game.player, 'dx', 0),
            pg.K_s: lambda: setattr(game.player, 'dy', 0),
            pg.K_d: lambda: setattr(game.player, 'dx', 0),
        }

    def save(self):
        pass

    def load(self):
        pass

