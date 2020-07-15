import src.data as data
import sys
from src.enemy import *
from src.view import *
from src.player import *
from src.ai import *
from random import randint, choice

assert pg.version.ver[0] == str(2), "Pygame version not compatible with the project"


# Note: Scroll by several pixels per update. The flip() method is very slow.
# Note: No cyclic dependencies, no going up hierarchy
# Separate handling of rects and updating from blitting. It can cause screen tearing
# Don't poke into other systems while writing code, use base class's methods
# Work on decoupling parts of code as much as you can
# TODO: Implement background moving to respond to a view
# TODO: Fix diagonal player movement being faster by 1.4 using angles
# TODO: Set font
# TODO: Handle the problem with Windows DPI scaling
# TODO: Add normal stats for player
# TODO: Implement message queues
# TODO: As it is, the current object system is broken completely. Implement separate class for objects that handles
# creation and destruction gracefully.


class Game:
    """Main game class"""

    def __init__(self):
        self.time = 1.0  # Adjust time speed (for slowmo)
        self.player = Player(data.SCREEN_WIDTH // 2,
                             data.SCREEN_HEIGHT // 2,
                             KeybordControllableAI(None),
                             [], 1000000, 7, 1)  # TODO: Temp
        self.player.ai.owner = self.player
        data.entities.add(self.player)
        self.view = View(self.player, data.screen)  # follow the player on the game's screen
        self.clock = pg.time.Clock()
        self.fps = data.FPS
        self.font = pg.font.Font(None, 40)
        self.mouse_pos = pg.mouse.get_pos()

    def main(self):
        """Run the game"""
        data.load(self)
        data.SFX.music.set_volume(data.defs['music_volume'])
        data.SFX.music.play(-1, 0, 1000)
        data.entities.add(self.spawn_mob(self.player, 'crawler', 1000, 200))
        data.entities.add(self.spawn_mob(self.player, 'wizard', 1000, 500))
        while True:
            self._process_events()
            # After every event
            self._update()
            self._draw()
            self.clock.tick(data.FPS)  # cap the fps
            self.fps = int(self.clock.get_fps())

    def _process_events(self):
        """Handle the event queue"""
        for event in pg.event.get():
            try:
                if event.type == pg.QUIT:
                    self.quit()
                elif event.type == pg.KEYDOWN:
                    data.keydown_actions[event.key]()  # execute specified keydown actions
                elif event.type == pg.KEYUP:
                    data.keyup_actions[event.key]()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    data.keydown_actions[event.button]()
            except KeyError:
                pass
            # On every event

    def _draw(self):
        """Draw every object and refresh the screen"""
        data.screen.fill((50, 50, 50))  # fill the void
        self.blit_rects()
        data.entities.draw(data.screen)
        data.objects.draw(data.screen)
        self.print_debug_info()
        pg.display.flip()

    def _update(self):
        self.mouse_pos = pg.mouse.get_pos()
        data.entities.update()
        data.objects.update()

    #    self.player.rect.x, self.player.rect.y = self.view.update((data.screen_width, data.screen_height),
    #                                                              self.mouse_pos,
    #                                                             (self.player.rect.x, self.player.rect.y))

    def spawn_mob(self, target, mob_type='', x=None, y=None):
        if not mob_type:
            mob_type = choice(('crawler', 'wizard'))
        hp_range = (1, 10)
        defence_range = (0, 5)
        speed_range = (1, self.player.speed // 2)
        way_x = choice((1, -1))  # choose which way we'll go
        way_y = choice((1, -1))
        # TODO: I am too stupid do write a better algorithm
        if x is None or y is None:
            x = target.x + way_x * randint(target.rect.width * 3, data.SCREEN_WIDTH // 2)
            y = target.y + way_y * randint(target.rect.height * 3, data.SCREEN_HEIGHT // 2)
        # the mob appears at a certain distance from the target,
        # but not less than a constant amount of its sizes
        # and no more than one screen away
        if mob_type == 'crawler':
            return Crawler(data.crawler_spritepack,
                           data.SFX.meat,
                           target,
                           x,
                           y,
                           randint(hp_range[0], hp_range[1]),
                           randint(defence_range[0], defence_range[1]),
                           randint(speed_range[0], speed_range[1]))
        elif mob_type == 'wizard':
            return Wizard(x, y, target, 500,  # TODO: TEMPORARY
                          randint(hp_range[0], hp_range[1]),
                          randint(speed_range[0], speed_range[1]), 300)  # TODO: Temporary

    def print_debug_info(self):
        text = self.font.render(f"X: {self.player.x} Y: {self.player.y} FPS: {self.fps}",
                                True, (255, 255, 255), (0, 0, 0))
        data.screen.blit(text, (10, 10))

    def blit_rects(self):
        def blit_box(obj, color):
            box = pg.Surface(obj.rect.size)
            box.fill(color)
            data.screen.blit(box, obj.rect)

        for orb in self.player.orbs:
            blit_box(orb, (255, 0, 255))
        for o in data.entities:
            blit_box(o, (100, 100, 100))
        for o in data.objects:
            blit_box(o, (255, 0, 0))

    @staticmethod
    def quit():
        data.save()
        sys.exit()

    def add_orb(self, color=''):
        if not color:
            color = choice(['green', 'blue', 'yellow'])
        self.player.add_orb(color)

    def del_orb(self):
        self.player.pop_orb()

    def cast_spell(self, spell: str):
        if spell == 'orb':
            angle = angle_to(pg.Vector2(self.mouse_pos), self.player)
            self.player.release_orb(angle)


if __name__ == '__main__':
    game = Game()
    game.main()
