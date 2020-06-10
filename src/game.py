from src.util import *


class Game:
    """Class to make all the necessary variables visible"""
    # TODO: Change cursor
    # TODO: Change icon : pygame.display.set_icon
    # TODO: Set font
    # TODO: pygame.display.toggle_fullscreen
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))  # get the screen
        pygame.display.set_caption("Ninja")
        self.bg = 11, 102, 32
        self.time = 1.0  # Adjust time speed
        self.data = Data("settings.json")

    def run(self):
        """Run the game"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # On every event

            # After  every event
            self.screen.fill(self.bg)
            pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()
