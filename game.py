from src.data import *
from src.object import *
from src.view import *
from src.misc import *

# Note: Always use .convert() when loading images from the disk
# Note: Scroll by several pixels per update. The flip() method is very slow.
# Note: No cyclic dependencies, no going up hierarchy

# TODO: Set font
# TODO: Add exception handling for files
# TODO: Handle the difficulties with object size etc depending on screen size. Add zoom?
# TODO: Add normal speed config for owner

import pathlib
print(pathlib.Path().absolute())
class Game:
    """Main game class"""

    def __init__(self):
        pg.mixer.pre_init(44100)
        pg.init()
        pg.mixer.set_num_channels(32)
        infos = pg.display.Info()
        self.screen_width, self.screen_height = infos.current_w, infos.current_h
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption("Ninja")
        pg.display.set_icon(load_image('icon.png')[0])
        self.bg, self.bg_rect = load_image("bg_test.png")
        self.bg = pg.transform.scale2x(self.bg)
        self.time = 1.0  # Adjust time speed
        self.data = Data(self, "settings.json")
        self.player = Player(self)
        self.view = View(self.player, self.screen)  # follow the player on the game's screen
        self.clock = pg.time.Clock()
        self.mouse_pos = pg.mouse.get_pos()
        self.objects = pg.sprite.Group()  # store ALL the objects in the game except single-instance ones

    def main(self):
        """Run the game"""
        while True:
            self._process_events()
            # After every event
            self._update()
            self._draw()
            self.clock.tick(self.data.fps)  # cap the fps

    def _process_events(self):
        """Handle the event queue"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                try:
                    self.data.keydown_actions[event.key]()  # execute specified keydown actions
                except KeyError:
                    pass
            elif event.type == pg.KEYUP:
                try:
                    self.data.keyup_actions[event.key]()
                except KeyError:
                    pass
            # On every event

    def _draw(self):
        """Draw every object and refresh the screen"""
        self._draw_bg()
        self.player.blit()
        self.print_text()
        pg.display.flip()

    def _update(self):
        self.mouse_pos = pg.mouse.get_pos()
        self.player.update()
    #    self.player.rect.x, self.player.rect.y = self.view.update((self.screen_width, self.screen_height),
    #                                                              self.mouse_pos,
    #                                                             (self.player.rect.x, self.player.rect.y))

    def print_text(self):
        font = pg.font.Font(None, 20)
        text = font.render('player coords ' + str(self.player.x) + '  ' + str(self.player.y), True, (0, 0, 0))
        self.screen.blit(text, (400, 300))

    def _draw_bg(self):
        self.screen.fill((0, 0, 0))  # fill the void
        self.screen.blit(self.bg, self.bg_rect)  # draw the image


# TODO: Change the annoying return of load_sprite, load_sound
# TODO: Implement background moving to respond to a view
if __name__ == '__main__':
    game = Game()
    game.main()
