import pygame
from .window import Window
from .fps import Tick
from data.e.scripts.tiles.tile_map import TileMap
from data.e.scripts.entities.ents import EntityManager

class World:
    def __init__(self, app):
        self.app = app
        self.window = Window(app, shaders=self.app.shaders)
        self.tile_map = TileMap(app)
        self.tick = Tick(app, fps=self.app.fps)
        self.gfx_manager = GFXManager(app)
        self.entity_manager = EntityManager(app)