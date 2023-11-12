import pygame, math

from ..tools.utils import load_chunks

class TileChunker:
    def __init__(self, tiles, chunk_size, tile_size):
        self.tiles = list(tiles)
        self.chunk_size = chunk_size
        self.tile_size = tile_size
        self.chunk_data = load_chunks(self.tiles, self.tile_size, self.chunk_size, {})
    
    def draw(self, surf, scroll):
        for y in range(math.ceil(surf.get_height() / (self.chunk_size.y * self.tile_size)) + 1):
            for x in range(math.ceil(surf.get_width() / (self.chunk_size.x * self.tile_size)) + 1):
                target_x = x - 1 + math.ceil(scroll.x / (self.chunk_size.x * self.tile_size))
                target_y = y - 1 + math.ceil(scroll.y / (self.chunk_size.y * self.tile_size))
                target_chunk = f'{target_x};{target_y}'
                if target_chunk in self.chunk_data:
                    for tile in self.chunk_data[target_chunk]:
                        tile.draw(surf, scroll)


