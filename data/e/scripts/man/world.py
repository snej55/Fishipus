from .window import Window # hello
from .fps import Tick
from ..env.tiles import TileMap
from ..entities.ents import EntityManager # hey
from ..gfx.management import GFXManager

class World:
    def __init__(self, app):
        self.app = app
        self.window = Window(app) # hey
        self.tile_map = TileMap(app)
        self.tick = Tick(app, fps=self.app.fps)
        self.gfx_manager = GFXManager(app)
        self.entity_manager = EntityManager(app)
    
    def update(self, shade_uniforms={}):
        screen, scroll = tuple(self.window.sec())
        self.tile_map.draw_decor(screen, scroll)
        self.entity_manager.update(screen, scroll)
        self.tile_map.update_grass([self.app.player.rect()])
        self.tile_map.draw_tiles(screen, scroll)
        self.app.update(screen, scroll)
        self.gfx_manager.update(screen, scroll)
        #pygame.display.set_caption(f'{self.app.title} at {self.tick.clock.get_fps() :.0f} FPS')
        self.window.shade(shade_uniforms)
        self.window.inflate()
        self.tick.update()