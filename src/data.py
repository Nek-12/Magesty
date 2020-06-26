from src.util import *


def toggle_fullscreen(game):
    if platform.system() == 'Linux':
        pygame.display.toggle_fullscreen()
    else:
        game.screen = pygame.display.set_mode((game.screen_width, game.screen_height))


class Data:
    def __init__(self, fname):
        # Mock-up entries before settings are implemented
        self.fps = 60
        self.player_max_hp = 100
        self.player_sprite = load_sprite("ninja.png")
        self.player_defence = 1
        self.settings_d = {
            pygame.K_F11: toggle_fullscreen,
            pygame.K_ESCAPE: sys.exit
        }

    def save(self):
        pass

    def load(self):
        pass

