import pygame

from data.e.scripts.bip import *
from .mgl.mgl import MGL
from .camera import Camera

class Window:
    def __init__(self, app, shaders={'frag': None, 'vert': None}):
        self.render_scale = pygame.Vector2(RENDER_SCALE, RENDER_SCALE)
        self.display = pygame.display.set_mode(WIN_DIMENSIONS, flags=pygame.DOUBLEBUF | pygame.OPENGL)
        self.screen = pygame.Surface((self.display.get_width() / self.render_scale.x, self.display.get_height() / self.render_scale.y))
        self.alpha_surf = self.screen.copy()
        self.app = app#
        self.camera = Camera(app, self)
        self.scroll = self.camera.scroll
        self.render_scroll = [0, 0]
        self.mgl = MGL(app, frag_path=shaders['frag'], vert_path=shaders['vert'])
    
    def set_camera_target(self, target):
        self.camera.target = target
    
    def sec(self):
        self.screen.fill((0, 0, 0))
        self.alpha_surf.fill((0, 0, 0))
        self.render_scroll = self.camera.update()
        return self.screen, self.render_scroll
    
    def draw(self, objects):
        for obj in objects:
            render_obj = getattr(self.app.world, obj)
            render_obj.draw(self.screen, self.render_scroll)
    
    def shade(self, uniforms):
        self.mgl.draw(self.screen, uniforms)
    
    def inflate(self, scale=0):
        pygame.transform.scale_by(self.screen, self.render_scale, self.display)
        pygame.display.flip()