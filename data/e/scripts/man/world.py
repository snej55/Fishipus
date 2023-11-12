import pygame
from .window import Window
from .fps import Tick
from ..env.tiles import TileMap
from ..entities.ents import EntityManager
from ..gfx.management import GFXManager

class World:
    def __init__(self, app):
        self.app = app
        self.window = Window(app)
        self.tile_map = TileMap(app)
        self.tick = Tick(app, fps=self.app.fps)
        self.gfx_manager = GFXManager(app)
        self.entity_manager = EntityManager(app)
    
    def update(self, shade_uniforms={}):
        screen, scroll = tuple(self.window.sec())
        self.tile_map.draw(screen, scroll)
        self.entity_manager.update(screen, scroll)
        self.app.update(screen, scroll)
        self.gfx_manager.update(screen, scroll)
        pygame.display.set_caption(f'{self.app.title} at {self.tick.clock.get_fps() :.0f} FPS')
        self.window.shade(shade_uniforms)
        self.window.inflate(scale=1.0)
        self.tick.update()