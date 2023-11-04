import pygame, sys, time, json

from data.e.scripts.init import *
from data.e.scripts.bip import *
from data.e.scripts.assets import *
from data.e.scripts.gfx.management import GFXManager
from data.e.scripts.man.camera import Camera
from data.e.scripts.man.window import Window
from data.e.scripts.env.tiles import TileMap
from data.e.scripts.entities.ents import EntityManager
from data.e.scripts.man.world import World

class Pengine:
    def __init__(self, mode='game', config={}):
        self.render_scale = pygame.Vector2(RENDER_SCALE, RENDER_SCALE)
        self.config = config
        self.clock = pygame.time.Clock()
        self.dt = 1
        self.title = 'pge window'
        if 'caption' in self.config:
            self.title = self.config['caption']
        self.mode = mode
        self.last_time = time.time() - 1 / 60
        self.tile_size = TILE_SIZE
        self.chunk_size = pygame.Vector2(CHUNK_SIZE)
        self.auto_tile_types = AUTO_TILE_TYPES
        self.physics_tile_types = PHYSICS_TILE_TYPES
        self.entity_quad_size = ENTITY_QUAD_SIZE
        self.danger = DANGER
        self.scrolling = 0
        self.render_scroll = [0, 0]
        self.screen_shake = 0
        self.clicking = False
        self.right_clicking = False
        self.mouse_pos = []
        self.assets = {'game': GAME_ASSETS, 'edit': EDIT_ASSETS}
        self.running = True
        self.keys = {key: False for key in KEYS}
        self.tile_map = TileMap(self)
        self.toggles = {}
        self.fps = 0
        self.shaders = {'frag': None, 'vert': None}
        for prgram in self.shaders:
            if prgram in self.config:
                self.shaders[prgram] = self.config[prgram]
        self.shaders = {'frag': self.shaders['frag'], 'vert': self.shaders['vert']}
        self.window = Window(self)
        self.camera = self.window.camera
        self.scroll = self.camera.scroll
        self.world = World(self)
        self.time = 0
    
    def load_level(self, path):
        return self.tile_map.load(path)
    
    def close(self):
        self.running = False
        print('closing')
        pygame.quit()
        sys.exit()
    
    def update(*args, **kwargs):
        pass
    
    def run(self):
        while self.running:
            self.time += 1 * self.dt / self.world.tick.slomo
            self.mouse_pos = list(n / self.render_scale[i] for i, n in enumerate(pygame.mouse.get_pos()))
            self.toggles = set([])
            self.scrolling = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                if event.type == pygame.KEYDOWN:
                    self.keys[event.key] = True
                    self.toggles.add(event.key)
                if event.type == pygame.KEYUP:
                    self.keys[event.key] = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                    if event.button == 3:
                        self.right_clicking = True
                    if event.button == 4:
                        self.scrolling = -1
                    if event.button == 5:
                        self.scrolling = 1
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False
            if self.keys[pygame.K_ESCAPE]:
                self.close()
            if self.mode == 'edit':
                self.render_scroll = self.camera.update()
                self.tile_map.draw(self.screen, self.render_scroll)
                self.update()
                self.entity_manager.update(self.screen, self.render_scroll)
                self.gfx_manager.update(self.screen, self.render_scroll)
                pygame.transform.scale_by(self.screen, self.render_scale, self.display)
                pygame.display.set_caption(self.title + ' at ' f'{self.clock.get_fps() :.1f} FPS!')
                pygame.display.flip()
                self.clock.tick(self.fps)
            else:
                self.world.update(shade_uniforms={'noise': self.world.window.screen, 'time': self.time})
                self.dt = self.world.tick.dt
