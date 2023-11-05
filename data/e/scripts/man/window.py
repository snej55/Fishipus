import pygame

from data.e.scripts.bip import *
from .mgl.mgl import MGL
from .camera import Camera

class Window:
    def __init__(self, app, shaders={'frag': None, 'vert': None}):
        self.render_scale = pygame.Vector2(RENDER_SCALE, RENDER_SCALE)
        self.display = pygame.display.set_mode(WIN_DIMENSIONS, flags=pygame.DOUBLEBUF | pygame.OPENGL)
        self.screen = pygame.Surface((self.display.get_width() / self.render_scale.x, self.display.get_height() / self.render_scale.y))
        self.app = app#
        self.camera = Camera(app, self)
        self.scroll = self.camera.scroll
        self.render_scroll = [0, 0]
        self.mgl = MGL(app, frag_path=shaders['frag'], vert_path=shaders['vert'])
    
    def set_camera_target(self, target):
        self.camera.target = target
    
    def sec(self):
        self.screen.fill((0, 0, 0))
        self.render_scroll = self.camera.update()
        return self.screen, self.render_scroll
    
    def draw(self, objects):
        for obj in objects:
            render_obj = getattr(self.app.world, obj)
            render_obj.draw(self.screen, self.render_scroll)
    
    def shade(self, uniforms):
        self.mgl.draw(self.screen, uniforms)
    
    def inflate(self, scale=0):
        scale = scale if scale else self.render_scale
        scaled_surf = pygame.transform.scale_by(self.screen, scale)
        self.display.blit(scaled_surf, (-(scaled_surf.get_width() - self.display.get_width()) * 0.5, -(scaled_surf.get_height() - self.display.get_height()) * 0.5))
        pygame.display.flip()