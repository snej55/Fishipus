# TODO: Camera stuff, zoom, slomo etc here
import pygame, random

class Camera:
    def __init__(self, app, target=None):
        self.scroll = pygame.Vector2(0, 0)
        self.render_scroll = [0, 0]
        self.screen_shake = 0
        self.target = target
        self.app = app
    
    def update(self):
        if self.target:
            self.scroll[0] += ((self.target.rect().centerx - self.app.screen.get_width() * 0.5 - self.scroll[0]) / 10) * 0.4 * self.app.dt
            self.scroll[1] += ((self.target.rect().centery - self.app.screen.get_height() * 0.5 - self.scroll[1]) / 12) * 0.4 * self.app.dt
        self.screen_shake = max(0, self.screen_shake - 1 * self.app.dt)
        screen_shake_offset = (random.random() * self.screen_shake - self.screen_shake / 2, random.random() * self.screen_shake - self.screen_shake / 2)
        self.render_scroll = pygame.Vector2(max(0, int(self.scroll[0] + screen_shake_offset[0])), int(self.scroll[1] + screen_shake_offset[1]))
        return self.render_scroll