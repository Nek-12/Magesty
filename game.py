import sys
from src.data import *
from src.object import *
from src.view import *
from src.misc import *
from src.enemy import *
assert pg.version.ver[0] == str(2), "Pygame version not compatible with the project"

# Note: Always use .convert() when loading images from the disk
# Note: Scroll by several pixels per update. The flip() method is very slow.
# Note: No cyclic dependencies, no going up hierarchy

# TODO: Fix diagonal player movement being faster by 1.4 using angles
# TODO: Set font
# TODO: Handle the problem with Windows DPI scaling
# TODO: Add normal speed config for player
# TODO: Fix the problem with sprites and colorkeys (transparent parts of images)


class Game:
    """Main game class"""
    def __init__(self):
        pg.mixer.pre_init()
        pg.init()
        pg.mixer.set_num_channels(32)
        infos = pg.display.Info()
        self.screen_width, self.screen_height = infos.current_w, infos.current_h
        self.screen = pg.display.set_mode((369*4, 209*4), pg.SCALED | pg.DOUBLEBUF)  # NOTE: temporary
        pg.display.set_caption("Ninja")
        pg.display.set_icon(load_image('icon.png')[0])
        self.bg, self.bg_rect = load_image("bg_test.png")
        self.bg = upscale_image(self.bg,4)  # animation consists of one frame
        self.time = 1.0  # Adjust time speed
        self.data = Data(self, "settings.json")
        self.player = Player(self)
        self.view = View(self.player, self.screen)  # follow the player on the game's screen
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, 40)
        self.fps = 0
        self.mouse_pos = pg.mouse.get_pos()
        self.entities = pg.sprite.Group()  # store ALL the objects in the game except single-instance ones

    def main(self):
        """Run the game"""
        self.data.load(self)
        self.data.music.set_volume(self.data.volume)
        self.data.music.play(-1, 0, 1000)
        while True:
            self._process_events()
            # After every event
            self._update()
            self._draw()
            self.clock.tick(self.data.fps)  # cap the fps
            self.fps = int(self.clock.get_fps())

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
        self.player.blit(self.screen)
        self.entities.draw(self.screen)
        self.print_debug_info()
        pg.display.flip()

    def _update(self):
        self.mouse_pos = pg.mouse.get_pos()
        self.player.update()
        self.entities.update()
        if len(self.entities) < 5:
            self.entities.add(self.spawn_mob('crawler', self.player))
            # TODO: Not an interesting strategy
    #    self.player.rect.x, self.player.rect.y = self.view.update((self.screen_width, self.screen_height),
    #                                                              self.mouse_pos,
    #                                                             (self.player.rect.x, self.player.rect.y))

    def spawn_mob(self, mob_type, target):
        if mob_type == 'crawler':
            # choose which way we'll go
            hp_range = (1,10)
            defence_range = (0,5)
            speed_range = (1,self.player.speed+1)
            way_x, way_y = 0, 0
            while way_x == 0 and way_y == 0:
                way_x = choice((0, 1, -1))
                way_y = choice((0, 1, -1))
            # TODO: I am too stupid do write a better algorithm
            x = target.x + way_x*randint(target.rect.width*SAFEZONE_MULTIPLIER, self.screen_width)
            y = target.y + way_y*randint(target.rect.height*SAFEZONE_MULTIPLIER, self.screen_height)
            # the mob appears at a certain distance from the target,
            # but not less than a constant amount of its sizes
            # and no more than one screen away
            return Crawler(self.data.crawler_spritepack,
                           self.data.meat_sounds,
                           target,
                           x,
                           y,
                           randint(hp_range[0], hp_range[1]),
                           randint(defence_range[0], defence_range[1]),
                           randint(speed_range[0],speed_range[1]))

    def print_debug_info(self):
        text = self.font.render(f"X: {self.player.x} Y: {self.player.y} FPS: {self.fps}",
                                True, (255, 255, 255), (0, 0, 0))
        self.screen.blit(text, (10, 10))

    def _draw_bg(self):
        self.screen.fill((0, 0, 0))  # fill the void
        self.screen.blit(self.bg, self.bg_rect)  # draw the image


# TODO: Implement background moving to respond to a view
if __name__ == '__main__':
    game = Game()
    game.main()
