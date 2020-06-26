from src.util import *

# Note: Always use .convert() when loading images from the disk
# Note: Scroll by several pixels per update. The flip() method is very slow.

# TODO: Change cursor
# TODO: Set font
# TODO: Add exception handling for files

class Game:
    """Main game class"""

    def __init__(self):
        pygame.init()
        infos = pygame.display.Info()
        screen_width, screen_height = infos.current_w, infos.current_h
        self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)  # get the screen
        pygame.display.set_caption("Ninja")
        pygame.display.set_icon(pygame.image.load("../res/icon.png").convert())

        self.bg = 11, 102, 32
        self.time = 1.0  # Adjust time speed
        self.data = Data("settings.json")

    def run(self):
        """Run the game"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:   # leave game by pressing escape
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                # On every event

            # After  every event
            self.screen.fill(self.bg)

            pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()
