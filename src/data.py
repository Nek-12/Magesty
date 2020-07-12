from src.util import *
import json
from src.misc import *
from src.animation import *

# DEFAULT
defs = {
    'fps': 60,
    'volume': 0.1,
    'player_level': 1,
    'player_cash': 0,
    'player_xp': 0,
    'difficulty': 1,
    'player_items': [],
    'player_spells': ['flash', 'comet', 'wave', 'tornado']
}
SETTINGS_FNAME = 'settings.json'
MILLISECOND = 1000 // defs['fps']
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Temporary values before items are introduced
player_max_hp = 100
player_defence = 1
player_speed = 15

# PRE-INIT
pg.mixer.pre_init()
pg.init()
pg.mixer.set_num_channels(32)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SCALED | pg.DOUBLEBUF)

# init
swing_soundpack = SoundPack(load_soundlist('swing'))
meat_soundpack = SoundPack(load_soundlist('meat'))
music = load_sound('music.wav')
player_move_anims = load_animations_dictionary('char_move', (0, 0, 32, 32), 4, -1, 'loop')
for el in player_move_anims.values():  # for every SpriteAnim object
    el.upscale_frames(4)  # make bigger
player_idle_image = player_move_anims['d'].base_image
slash_anim = SpriteAnim(load_anim('slash_1', -1))
slash_anim.upscale_frames(2)
crawler_spritepack = load_sprite_dictionary('crawler', -1)
for k, v in crawler_spritepack.items():  # for every image
    crawler_spritepack[k] = upscale_image(v, 2)
green_orb_anim = load_animation_from_table('orbs', 'Small_Poisonball_9x25.png', 9, 25, 1, TIMINGS_FILENAME, 'loop')
green_orb_anim.upscale_frames(4)
yellow_orb_anim = load_animation_from_table('orbs', 'Small_Fireball_10x26.png', 10, 26, 1, TIMINGS_FILENAME, 'loop')
yellow_orb_anim.upscale_frames(4)
blue_orb_anim = load_animation_from_table('orbs', 'Small_Iceball_9x24.png', 9, 24, 1, TIMINGS_FILENAME, 'loop')
blue_orb_anim.upscale_frames(4)
keydown_actions = None  # blank until we load()
keyup_actions = None


def save(fname=SETTINGS_FNAME):
    """Dump the data into json file"""
    global defs
    f = open(fname, 'w')
    json.dump(defs, f, indent=4)
    pass


def load(game, fname=SETTINGS_FNAME):
    """Load the data from the json, alters the global variables. Call before using any of them"""
    global keydown_actions, keyup_actions, defs
    try:
        f = open(fname)
        defs = json.load(f)
    except FileNotFoundError:
        print("The settings file was not found. Using default values...")
    keydown_actions = {
        pg.K_F12: game.quit,
        pg.K_w: lambda: setattr(game.player, 'moving_u', True),
        pg.K_a: lambda: setattr(game.player, 'moving_l', True),
        pg.K_s: lambda: setattr(game.player, 'moving_d', True),
        pg.K_d: lambda: setattr(game.player, 'moving_r', True),
        pg.K_SPACE: game.cast_spell
    }
    # P.S. We can't use assignment in lambdas
    keyup_actions = {
        pg.K_w: lambda: setattr(game.player, 'moving_u', False),
        pg.K_a: lambda: setattr(game.player, 'moving_l', False),
        pg.K_s: lambda: setattr(game.player, 'moving_d', False),
        pg.K_d: lambda: setattr(game.player, 'moving_r', False),
    }
