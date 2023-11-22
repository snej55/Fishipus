import pygame, json

from ..assets import GAME_ASSETS

class LeafSpawnLoader:
    def __init__(self, app, path='data/config/leaf.json'):
        self.config = {}
        for mode in GAME_ASSETS:
            if 'decor' in str(mode).lower():
                self.config[mode] = {}
                for variant, img in enumerate(GAME_ASSETS[mode]):
                    self.config[mode][variant] = [img, None, (0, 0)]
        self.app = app
        self.rects = self.load(path)
      
    def load(self, path):
        with open(path, 'r') as f:
            leaf_data = json.load(f)
            rect_data = []
            tile_map = self.app.world.tile_map
            id_pairs = [(m, v) for m in self.config for v in self.config[m]]
            for tile in tile_map.extract(id_pairs, keep=True):
                if leaf_data[tile.mode][str(tile.variant)][0]:
                    rect_data.append((pygame.Rect(tile.rect.x + leaf_data[tile.mode][str(tile.variant)][0][0], tile.rect.y + leaf_data[tile.mode][str(tile.variant)][0][1], leaf_data[tile.mode][str(tile.variant)][0][2], leaf_data[tile.mode][str(tile.variant)][0][3]), False))
            return rect_data
            
