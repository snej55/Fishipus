import pygame, sys, time, json

from data.e.scripts.init import *
from data.e.scripts.bip import *
from data.e.scripts.assets import *
from data.e.scripts.gfx.management import GFXManager
from data.e.scripts.man.camera import Camera
from data.e.scripts.env.tiles import TileMap

class Pengine:
    def __init__(self, mode='game'):
        self.render_scale = pygame.Vector2(RENDER_SCALE, RENDER_SCALE)
        self.display = pygame.display.set_mode(WIN_DIMENSIONS)
        self.screen = pygame.Surface((self.display.get_width() / self.render_scale.x, self.display.get_height() / self.render_scale.y))
        self.clock = pygame.time.Clock()
        self.dt = 1
        self.title = 'Rogue Bottoms'
        self.last_time = time.time() - 1 / 60
        self.fps = 0
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
        self.gfx_manager = GFXManager(self)
        self.camera = Camera(self, None)
        self.scroll = self.camera.scroll
    
    def load_level(self, path):
        return self.tile_map.load(path)
    
    def close(self):
        self.running = False
        print('closing')
        pygame.quit()
        sys.exit()
    
    def update(self):
        pass
    
    def run(self):
        while self.running:
            self.dt = time.time() - self.last_time
            self.dt *= 60
            self.last_time = time.time()
            self.mouse_pos = list(n / self.render_scale[i] for i, n in enumerate(pygame.mouse.get_pos()))
            self.screen.fill((0, 0, 0))
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
            self.render_scroll = self.camera.update()
            self.tile_map.draw(self.screen, self.render_scroll)
            self.update()
            self.gfx_manager.update(self.screen, self.render_scroll)
            pygame.transform.scale_by(self.screen, self.render_scale, self.display)
            pygame.display.set_caption(self.title + ' at ' f'{self.clock.get_fps() :.1f} FPS!')
            pygame.display.flip()
            self.clock.tick(self.fps)
