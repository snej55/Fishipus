import pygame

from data.e.scripts.bip import *
from .mgl.mgl import MGL
from .camera import Camera

class Window:
    def __init__(self, app):
        self.render_scale = pygame.Vector2(RENDER_SCALE, RENDER_SCALE)
        self.display = pygame.display.set_mode(WIN_DIMENSIONS, flags=pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)
        self.screen = pygame.Surface((self.display.get_width() / self.render_scale.x, self.display.get_height() / self.render_scale.y))
        self.alpha_surf = self.screen.copy()
        self.app = app#
        self.camera = Camera(app, self)
        self.scroll = self.camera.scroll
        self.render_scroll = [0, 0]
        self.vaos = {}
        self.mgl = MGL(app)
    
    def add_shader(self, name, frag_path, vert_path=None, buffer=None, vao_args=['2f 2f', 'vert', 'texcoord']):
        self.vaos[name] = self.mgl.render_object(frag_path, vert_path, vao_args, buffer)
    
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
    
    def shade(self, uniforms, dest=None):
        for vao in self.vaos:
            rdest = None
            if dest:
                if vao in dest:
                    rdest = dest[vao]
            self.vaos[vao].render(rdest, uniforms[vao])
    
    def inflate(self, scale=0):
        pygame.transform.scale_by(self.screen, self.render_scale, self.display)
        pygame.display.flip()