import src.data as data
import sys
from random import randint, choice
from src.enemy import *
from src.view import *
from src.player import *

assert pg.version.ver[0] == str(2), "Pygame version not compatible with the project"


# Note: Scroll by several pixels per update. The flip() method is very slow.
# Note: No cyclic dependencies, no going up hierarchy
# Separate handling of rects and updating from blitting. It can cause screen tearing

# TODO: Implement background moving to respond to a view
# TODO: Fix diagonal player movement being faster by 1.4 using angles
# TODO: Set font
# TODO: Handle the problem with Windows DPI scaling
# TODO: Add normal stats for player
# TODO: Implement message queues


class Game:
    """Main game class"""

    def __init__(self):
        self.time = 1.0  # Adjust time speed (for slowmo)
        self.player = Player()
        self.view = View(self.player, data.screen)  # follow the player on the game's screen
        self.clock = pg.time.Clock()
        self.fps = data.defs['fps_cap']
        self.font = pg.font.Font(None, 40)
        self.mouse_pos = pg.mouse.get_pos()
        self.entities = pg.sprite.Group()  # store ALL the entities
        self.objects = pg.sprite.Group()  # store all the other things

    def main(self):
        """Run the game"""
        data.load(self)
        data.music.set_volume(data.defs['volume'])
        data.music.play(-1, 0, 1000)
        while True:
            self._process_events()
            # After every event
            self._update()
            self._draw()
            self.clock.tick(data.defs['fps_cap'])  # cap the fps
            self.fps = int(self.clock.get_fps())

    def _process_events(self):
        """Handle the event queue"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            elif event.type == pg.KEYDOWN:
                try:
                    data.keydown_actions[event.key]()  # execute specified keydown actions
                except KeyError:
                    pass
            elif event.type == pg.KEYUP:
                try:
                    data.keyup_actions[event.key]()
                except KeyError:
                    pass
            # On every event

    def _draw(self):
        """Draw every object and refresh the screen"""
        data.screen.fill((50, 50, 50))  # fill the void
        self.blit_rects()
        self.player.blit(data.screen)
        self.entities.draw(data.screen)
        self.objects.draw(data.screen)
        self.print_debug_info()
        pg.display.flip()

    def _update(self):
        self.mouse_pos = pg.mouse.get_pos()
        self.player.update()
        self.entities.update()
        self.objects.update()
        if len(self.entities) < 5:
            self.entities.add(self.spawn_mob('crawler', self.player))
            # TODO: Not an interesting strategy

    #    self.player.rect.x, self.player.rect.y = self.view.update((data.screen_width, data.screen_height),
    #                                                              self.mouse_pos,
    #                                                             (self.player.rect.x, self.player.rect.y))

    def spawn_mob(self, mob_type, target):
        if mob_type == 'crawler':
            # choose which way we'll go
            hp_range = (1, 10)
            defence_range = (0, 5)
            speed_range = (1, self.player.speed // 2)
            way_x = choice((1, -1))
            way_y = choice((1, -1))
            # TODO: I am too stupid do write a better algorithm
            x = target.x + way_x * randint(target.rect.width * SAFEZONE_MULTIPLIER, data.SCREEN_WIDTH)
            y = target.y + way_y * randint(target.rect.height * SAFEZONE_MULTIPLIER, data.SCREEN_HEIGHT)
            # the mob appears at a certain distance from the target,
            # but not less than a constant amount of its sizes
            # and no more than one screen away
            return Crawler(data.crawler_spritepack,
                           data.meat_soundpack,
                           target,
                           x,
                           y,
                           randint(hp_range[0], hp_range[1]),
                           randint(defence_range[0], defence_range[1]),
                           randint(speed_range[0], speed_range[1]))

    def print_debug_info(self):
        text = self.font.render(f"X: {self.player.x} Y: {self.player.y} FPS: {self.fps}     "
                                f"E - add orb, Q  - remove orb",
                                True, (255, 255, 255), (0, 0, 0))
        data.screen.blit(text, (10, 10))

    def blit_rects(self):
        def blit_box(obj, color):
            box = pg.Surface(obj.rect.size)
            box.fill(color)
            data.screen.blit(box, obj.rect)

        blit_box(self.player, (255, 255, 255))
        # blit_box(self.player.anim, (0, 0, 0))
        for orb in self.player.orbs:
            blit_box(orb, (255, 0, 255))
        for o in self.entities:
            blit_box(o, (100, 100, 100))
        for o in self.objects:
            blit_box(o, (255, 0, 0))

    @staticmethod
    def quit():
        data.save()
        sys.exit()

    def add_orb(self, color=choice(['green', 'blue', 'yellow'])):
        self.player.add_orb(color)

    def del_orb(self):
        self.player.del_orb()

    def cast_spell(self):
        pass


if __name__ == '__main__':
    game = Game()
    game.main()
