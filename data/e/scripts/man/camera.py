# TODO: Camera stuff, zoom, slomo etc here
import pygame, random, perlin_noise

noise = perlin_noise.PerlinNoise(octaves=10, seed=1)

class Camera:
    def __init__(self, app, window, target=None):
        self.scroll = pygame.Vector2(0, 0)
        self.render_scroll = [0, 0]
        self.screen_shake = 0
        self.target = target
        self.window = window
        self.app = app
    
    def add_screen_shake(self, amount):
        amount *= 0.5
        self.screen_shake = min(16, max(self.screen_shake, (amount * 2 + self.screen_shake) * 0.5))
    
    def update(self):
        if self.target:
            self.scroll[0] += ((self.target.rect().centerx - self.window.screen.get_width() * 0.5 - self.scroll[0]) / 10) * 0.4 * self.app.dt
            self.scroll[1] += ((self.target.rect().centery - self.window.screen.get_height() * 0.5 - self.scroll[1]) / 12) * 0.4 * self.app.dt
        self.screen_shake = max(0, self.screen_shake - 0.3 * self.app.dt)
        screen_shake_offset = (noise(self.app.time) * self.screen_shake - self.screen_shake / 2, noise(self.app.time) * self.screen_shake - self.screen_shake / 2)
        self.render_scroll = pygame.Vector2(max(0, int(self.scroll[0] + screen_shake_offset[0] ** 2)), int(self.scroll[1] + screen_shake_offset[1] ** 2))
        return self.render_scroll