import pygame, sys
from data.e.scripts.bip import *
from .camera import Camera

class Window:
    def __init__(self, app):
        self.render_scale = pygame.Vector2(RENDER_SCALE, RENDER_SCALE)
        self.display = pygame.display.set_mode(WIN_DIMENSIONS, flags=pygame.DOUBLEBUF | pygame.OPENGL)
        self.screen = pygame.Surface((self.display.get_width() / self.render_scale.x, self.display.get_height() / self.render_scale.y))
        self.app = app
        self.camera = Camera(app)
        self.scroll = self.camera.scroll
        self.render_scroll = [0, 0]
    
    def set_camera_target(self, target):
        self.camera.target = target
    
    def draw(self, objects):
        self.screen.fill((0, 0, 0))
        self.render_scroll = self.camera.update()
        for obj in objects:
            render_obj = getattr(self.app.world, obj)
            render_obj.draw(self.screen, self.render_scroll)