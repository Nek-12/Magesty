import json
from src.animation import *
from src.sound import *
from os import sep
# DEFAULT
# AFTER CHANGING DON'T FORGET TO DELETE settings.json!
defs = {
    'fps_cap': 60,
    'music_volume': 0.1,
    'sound_volume': 1,  # TODO: Noone uses it
    'player_level': 1,
    'player_cash': 0,
    'player_xp': 0,
    'difficulty': 1,
    'player_items': [],
    'max_orbs_player': 3,
    'player_spells': ['flash', 'comet', 'wave', 'tornado'],
    'keys': {
        'up': pg.K_w,
        'down': pg.K_s,
        'left': pg.K_a,
        'right': pg.K_d,
        'green orb': pg.K_q,
        'yellow orb': pg.K_e,
        'blue orb': pg.K_f,
        'remove orb': pg.K_r,
        'spell 1': pg.BUTTON_LEFT,
        'spell 2': pg.BUTTON_RIGHT,
        'spell 3': pg.K_SPACE,
        'pause': pg.K_ESCAPE,
    }
}
MS_PER_FRAME = 1000 / defs['fps_cap']
FRAMES_PER_MS = defs['fps_cap'] / 1000
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = defs['fps_cap']

# Temporary values before items are introduced
player_max_hp = 100
player_defence = 1
player_speed = 10

# PRE-INIT
# TODO: Bad idea. Refactor until you get proper entity factories
objects = pg.sprite.Group()
entities = pg.sprite.Group()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SCALED | pg.DOUBLEBUF)
pg.display.set_caption("Ninja")
pg.display.set_icon(load_image('icon.png'))
pg.mixer.pre_init()
pg.init()
pg.mixer.set_num_channels(32)


# INIT
class Anims:
    player_move = generate_animation_dict(Spritesheet('mage-light.png', -1).load_table(48, 64),
                                          generate_timings(3, 3))
    wizard_move = generate_animation_dict(Spritesheet('mage-dark.png', -1).load_table(48, 64),
                                          generate_timings(3, 3))
    green_orb = load_anim_from_table('orbs', 'Small_Poisonball_9x25.png',
                                     9, 25, -1, 1, 'loop').upscale(2)
    yellow_orb = load_anim_from_table('orbs', 'Small_Fireball_10x26.png',
                                      10, 26, -1, 1, 'loop').upscale(2)
    blue_orb = load_anim_from_table('orbs', 'Small_Iceball_9x24.png',
                                    9, 24, -1, 1, 'loop').upscale(2)
    yellow_orb_fly = load_anim_from_table('orbs', 'Fireball_68x9.png',
                                          68, 9, -1, 1, 'loop').upscale(3)
    green_orb_fly = load_anim_from_table('orbs', 'Poisonball_65x9.png',
                                         65, 9, -1, 1, 'loop').upscale(3)
    blue_orb_fly = load_anim_from_table('orbs', 'Iceball_84x9.png',
                                        84, 9, -1, 1, 'loop').upscale(3)
    small_explosion = load_anim_from_table('explosions', 'vertical_small_100x100.png',
                                           100, 100, -1, 1).upscale(2)
    explosion = load_anim_from_table('explosions', 'explosion_100x100.png',
                                     100, 100, -1, 1)
    vertical_explosion = load_anim_from_table('explosions', 'vertical_100x100.png',
                                              100, 100, -1, 1)
    x_plosion = load_anim_from_table('explosions', 'x-plosion_100x100.png',
                                     100, 100, -1, 1)

    vortex_explosion = load_anim_from_table('explosions', 'vortex_100x100.png',
                                            100, 100, -1, 1)


class SFX:
    swing = SoundPack('swing')
    meat = SoundPack('meat')
    music = load_sound('music.wav')
    orb_release = load_sound('orb_release.wav')
    orb_explode = load_sound('orb_explode.wav')


player_idle_image = Anims.player_move['d'].base_image
wizard_idle_image = Anims.wizard_move['d'].base_image
crawler_spritepack = load_sprite_dictionary('crawler', -1)
for k, v in crawler_spritepack.items():  # for every key, image
    crawler_spritepack[k] = upscale_image(v, 2)
crawler_spritepack['l'] = pg.transform.flip(crawler_spritepack['d'], True, False)
crawler_spritepack['r'] = crawler_spritepack['d']

keydown_actions = None  # blank until we load()
keyup_actions = None


def to_frames(ms):
    return ms * FRAMES_PER_MS


def to_ms(frames):
    return frames * MS_PER_FRAME


def save():
    """Dump the data into json file"""
    global defs
    f = open(f'..{os.sep}settings.json', 'w')
    json.dump(defs, f, indent=4)


def load(game):
    """Load the data from the json, alters the global variables. Call before using any of them"""
    global keydown_actions, keyup_actions, defs
    try:
        f = open(f'..{os.sep}settings.json')
        defs = json.load(f)
    except FileNotFoundError:
        print("The settings file was not found. Using default values...")
    # dispatch table
    mv = game.player.ai.move
    st = game.player.ai.stop
    keydown_actions = {
        pg.K_F12: game.quit,
        defs['keys']['up']: lambda: mv('up'),
        defs['keys']['left']: lambda: mv('left'),
        defs['keys']['down']: lambda: mv('down'),
        defs['keys']['right']: lambda: mv('right'),
        defs['keys']['green orb']: lambda: game.add_orb('green'),
        defs['keys']['yellow orb']: lambda: game.add_orb('yellow'),
        defs['keys']['blue orb']: lambda: game.add_orb('blue'),
        defs['keys']['remove orb']: game.del_orb,
        defs['keys']['spell 1']: lambda: game.cast_spell('orb'),
    }
    # P.S. We can't use assignment in lambdas
    keyup_actions = {
        defs['keys']['up']: lambda: st('up'),
        defs['keys']['left']: lambda: st('left'),
        defs['keys']['down']: lambda: st('down'),
        defs['keys']['right']: lambda: st('right'),
    }
