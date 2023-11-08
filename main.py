import pygame, random
from data.e.scripts.pengine import Pengine
from data.e.scripts.env.tiles import *
from data.scripts.entities import Player, Blobbo
from data.scripts.sword import Sword

class App(Pengine):
    def __init__(self):
        super().__init__(config={
            'caption': 'JINJAMIJET',
            'frag': 'frag.glsl',
            'vert': 'vert.glsl'
        })
        self.world.tile_map.load('data/maps/0.json')
        self.player = Player((200, 10), (6, 7), (-1, -1), self, vj=-4)
        self.blobbo = [Blobbo((250 + i * 10, 100), (6, 7), (-1, -1), self, 'blobbo', health=5) for i in range(10)]
        self.world.window.set_camera_target(self.player)

    def update(self, screen, scroll):
        self.player.update()
        self.player.draw(screen, scroll)

if __name__ == '__main__':
    App().run()