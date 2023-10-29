import pygame, random
from data.e.scripts.pengine import Pengine
from data.e.scripts.env.tiles import *
from data.scripts.entities import Player
from data.scripts.sword import Sword

class App(Pengine):
    def __init__(self, path):
        super().__init__(path)
        self.tile_map = TileMap(self)
        self.tile_map.load('data/maps/0.json')
        self.title = 'JINJAMIJET'
        self.player = Player((200, 10), (6, 7), (-1, -1), self, vj=-4)
        self.camera.target = self.player

    def update(self):
        self.tile_map.draw(self.screen, self.render_scroll)
        self.player.update()
        self.player.draw(self.screen, self.render_scroll)

if __name__ == '__main__':
    App('data/e/init/init.json').run()