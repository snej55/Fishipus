import pygame, random
from data.e.scripts.pengine import Pengine
from data.e.scripts.env.tiles import *
from data.scripts.entities import Player, Blobbo
from data.scripts.sword import Sword

class App(Pengine):
    def __init__(self):
        super().__init__()
        self.tile_map.load('data/maps/0.json')
        self.title = 'JINJAMIJET'
        self.player = Player((200, 10), (6, 7), (-1, -1), self, vj=-4)
        self.camera.target = self.player
        self.blobbo = Blobbo((100, 100), (6, 7), (-1, -1), self, 'blobbo')

    def update(self):
        self.player.update()
        self.player.draw(self.screen, self.render_scroll)
        if pygame.K_p in self.toggles:
            print(len(self.player.get_colliding_ents()))

if __name__ == '__main__':
    App().run()