from src.util import *
from src.data import *
from src.object import *


# Note: Always use .convert() when loading images from the disk
# Note: Scroll by several pixels per update. The flip() method is very slow.
# Note: No cyclic dependencies, no going up hierarchy

# TODO: Set font
# TODO: Add exception handling for files
# TODO: Handle the difficulties with object size etc depending on screen size. Add zoom?
# TODO: Handle the framerate x movement problem. a) cap fps b) fps-independent
# TODO: Add dependencies on time
# TODO: Add normal speed config for player

class Game:
    """Main game class"""

    def __init__(self):
        pygame.init()
        infos = pygame.display.Info()
        self.screen_width, self.screen_height = infos.current_w, infos.current_h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Ninja")
        pygame.display.set_icon(pygame.image.load("../res/img/icon.png").convert())

        self.bg = 11, 102, 32  # RGB
        self.time = 1.0  # Adjust time speed
        self.data = Data("settings.json")
        self.player = Player(self.data.player_sprite,
                             self.screen_rect.x,
                             self.screen_rect.y,
                             self.data.player_max_hp,
                             self.data.player_defence,
                             10)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(1, 10)  # Repeat KEYDOWN events every 10 ms instead of one-time

    def main(self):
        """Run the game"""
        while True:
            self._process_events()
            # After every event
            self.player.update()
            self._draw()
            self.clock.tick(self.data.fps)  # <fps> times per second

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    sys.exit('KILLED')
                elif event.key == pygame.K_d:
                    self.player.x += self.player.speed
                elif event.key == pygame.K_a:
                    self.player.x -= self.player.speed
                elif event.key == pygame.K_w:
                    self.player.y -= self.player.speed  # TODO: Handle inverted values
                elif event.key == pygame.K_s:
                    self.player.y += self.player.speed
                elif event.key == pygame.K_F11:
                    toggle_fullscreen(self)
            # On every event

    def _draw(self):
        self.screen.fill(self.bg)  # blank the screen
        self.screen.blit(self.player.sprite, self.player.rect)
        pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.main()
