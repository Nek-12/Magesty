from src.util import *
import json
from src.misc import *
from src.animation import *

# DEFAULT
defs = {
    'fps_cap': 60,
    'volume': 0.1,
    'player_level': 1,
    'player_cash': 0,
    'player_xp': 0,
    'difficulty': 1,
    'player_items': [],
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
        'spell 1': pg.K_SPACE,
        'spell 2': pg.BUTTON_LEFT,
        'spell 3': pg.BUTTON_RIGHT,  # TODO: Confirm that these represent mouse buttons, i sorta guessed it
        'pause': pg.K_ESCAPE,
    }
}
SETTINGS_PATH = f'..{SEP}settings.json'
MILLISECOND = 1000 // defs['fps_cap']
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Temporary values before items are introduced
player_max_hp = 100
player_defence = 1
player_speed = 10

# PRE-INIT
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SCALED | pg.DOUBLEBUF)
pg.display.set_caption("Ninja")
pg.display.set_icon(load_image('icon.png'))
pg.mixer.pre_init()
pg.init()
pg.mixer.set_num_channels(32)

# INIT
swing_soundpack = SoundPack(load_soundlist('swing'))
meat_soundpack = SoundPack(load_soundlist('meat'))
music = load_sound('music.wav')
player_anims_list = Spritesheet('mage-light.png', -1).load_table(48, 64)
player_anims_timings = generate_timings(3, 3)
player_move_anims = {
    'u': SpriteAnim((player_anims_list[0:3], player_anims_timings), 'loop'),
    'r': SpriteAnim((player_anims_list[3:6], player_anims_timings), 'loop'),
    'd': SpriteAnim((player_anims_list[6:9], player_anims_timings), 'loop'),
    'l': SpriteAnim((player_anims_list[9:12], player_anims_timings), 'loop')
}
player_idle_image = player_move_anims['d'].base_image
# slash_anim = SpriteAnim(load_anim('slash_1', -1))
# slash_anim.upscale_frames(2)
crawler_spritepack = load_sprite_dictionary('crawler', -1)
for k, v in crawler_spritepack.items():  # for every key, image
    crawler_spritepack[k] = upscale_image(v, 2)
green_orb_anim = load_animation_from_table('orbs', 'Small_Poisonball_9x25.png', 9, 25, -1, 1, TIMINGS_FILENAME, 'loop')
green_orb_anim.upscale_frames(4)
yellow_orb_anim = load_animation_from_table('orbs', 'Small_Fireball_10x26.png', 10, 26, -1, 1, TIMINGS_FILENAME, 'loop')
yellow_orb_anim.upscale_frames(4)
blue_orb_anim = load_animation_from_table('orbs', 'Small_Iceball_9x24.png', 9, 24, -1, 1,  TIMINGS_FILENAME, 'loop')
blue_orb_anim.upscale_frames(4)
keydown_actions = None  # blank until we load()
keyup_actions = None


def save(fname=SETTINGS_PATH):
    """Dump the data into json file"""
    global defs
    f = open(fname, 'w')
    json.dump(defs, f, indent=4)


def load(game, fname=SETTINGS_PATH):
    """Load the data from the json, alters the global variables. Call before using any of them"""
    global keydown_actions, keyup_actions, defs
    try:
        f = open(fname)
        defs = json.load(f)
    except FileNotFoundError:
        print("The settings file was not found. Using default values...")
    # dispatch table
    keydown_actions = {
        pg.K_F12: game.quit,
        defs['keys']['up']: lambda: setattr(game.player, 'moving_u', True),
        defs['keys']['left']: lambda: setattr(game.player, 'moving_l', True),
        defs['keys']['down']: lambda: setattr(game.player, 'moving_d', True),
        defs['keys']['right']: lambda: setattr(game.player, 'moving_r', True),
        defs['keys']['green orb']: lambda: game.add_orb('green'),
        defs['keys']['yellow orb']: lambda: game.add_orb('yellow'),
        defs['keys']['blue orb']: lambda: game.add_orb('blue'),
        defs['keys']['remove orb']: game.del_orb
    }
    # P.S. We can't use assignment in lambdas
    keyup_actions = {
        defs['keys']['up']: lambda: setattr(game.player, 'moving_u', False),
        defs['keys']['left']: lambda: setattr(game.player, 'moving_l', False),
        defs['keys']['down']: lambda: setattr(game.player, 'moving_d', False),
        defs['keys']['right']: lambda: setattr(game.player, 'moving_r', False),
    }
