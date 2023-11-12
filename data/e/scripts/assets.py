import pygame

from .tools.utils import *
from .bip import *

GAME_ASSETS = {'large_decor': load_tile_imgs('decor/large_decor.png', 32),
               'gras': load_spritesheet('grass', 'grass'),
               'sword': load_img('entities/sword.png'),
               'slash': load_spritesheet('vfx', 'slash'),
               'noise': load_img('vfx/noise.png'),
               'particle/particle': load_spritesheet('particles', 'particle'),
               'particle/explode': load_spritesheet('particles', 'explode')}
EDIT_ASSETS = {'large_decor': load_tile_imgs('decor/large_decor.png', 32)}
GAME_ASSETS = load_tile_assets('tiles', GAME_ASSETS, TILE_SIZE)
EDIT_ASSETS = load_tile_assets('tiles', EDIT_ASSETS, TILE_SIZE)
load_entity_assets('entities/player', GAME_ASSETS, 'player')
load_entity_assets('entities/blobbo', GAME_ASSETS, 'blobbo')
PALETTES = load_palettes(GAME_ASSETS)