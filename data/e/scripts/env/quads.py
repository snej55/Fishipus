import math, pygame
from ..bip import *

# TODO: This was created in a rush. Update later.

class StationaryQuads:
  def __init__(self, items, chunk_size):
    self.items = list(items)
    self.chunk_size = pygame.Vector2(chunk_size)
    self.chunk_data = self.load_chunks(items, chunk_size)

  @staticmethod
  def load_chunks(items, chunk_dim):
    chunk_data = {}
    for item in items:
      loc = str(math.floor(item.pos[0] / chunk_dim[0] / TILE_SIZE)) + ';' + str(math.floor(item.pos[1] / chunk_dim[1] / TILE_SIZE))  # item must have attribute pos as a pygame.Vector2 or list
      if not loc in chunk_data:
        chunk_data[loc] = []
      chunk_data[loc].append(item)
    return chunk_data

  def add_item(item):
    loc = str(math.floor(item.pos[0] / self.chunk_dim[0] / TILE_SIZE)) + ';' + str(math.floor(item.pos[1] / self.chunk_dim[1] / TILE_SIZE))  # item must have attribute pos as a pygame.Vector2 or list
    if not loc in chunk_data:
      self.chunk_data[loc] = []
    self.chunk_data[loc].append(item)

  def update(self, surf, scroll, *args, **kwargs):
    for y in range(math.ceil(surf.get_height() / (self.chunk_size.y * TILE_SIZE)) + 1):
          for x in range(math.ceil(surf.get_width() / (self.chunk_size.x * TILE_SIZE)) + 1):
              target_x = x - 1 + math.ceil(scroll.x / (self.chunk_size.x * TILE_SIZE))
              target_y = y - 1 + math.ceil(scroll.y / (self.chunk_size.y * TILE_SIZE))
              target_chunk = f'{target_x};{target_y}'
              if target_chunk in self.chunk_data:
                  for item in self.chunk_data[target_chunk]:
                    item.update(*args, **kwargs)

class MovingQuads:
  def __init__(self, items, chunk_size):
    self.items = list(items)
    self.chunk_size = pygame.Vector2(chunk_size)
    self.chunk_data = self.load_chunks(items, chunk_size)

  @staticmethod
  def load_chunks(items, chunk_dim):
    chunk_data = {}
    for item in items:
      loc = str(math.floor(item.pos[0] / chunk_dim[0] / TILE_SIZE)) + ';' + str(math.floor(item.pos[1] / chunk_dim[1] / TILE_SIZE))  # item must have attribute pos as a pygame.Vector2 or list
      if not loc in chunk_data:
        chunk_data[loc] = []
      chunk_data[loc].append(item)
    return chunk_data

  def add_item(item):
    loc = str(math.floor(item.pos[0] / self.chunk_dim[0] / TILE_SIZE)) + ';' + str(math.floor(item.pos[1] / self.chunk_dim[1] / TILE_SIZE))  # item must have attribute pos as a pygame.Vector2 or list
    if not loc in chunk_data:
      self.chunk_data[loc] = []
    self.chunk_data[loc].append(item)

  def update(self, surf, scroll, *args, **kwargs):
    for y in range(math.ceil(surf.get_height() / (self.chunk_size.y * TILE_SIZE)) + 1):
          for x in range(math.ceil(surf.get_width() / (self.chunk_size.x * TILE_SIZE)) + 1):
              target_x = x - 1 + math.ceil(scroll.x / (self.chunk_size.x * TILE_SIZE))
              target_y = y - 1 + math.ceil(scroll.y / (self.chunk_size.y * TILE_SIZE))
              target_chunk = f'{target_x};{target_y}'
              if target_chunk in self.chunk_data:
                  for i, item in sorted(enumerate(self.chunk_data[target_chunk]), reverse=True):
                    item.update(*args, **kwargs)
                    loc = loc = str(math.floor(item.pos[0] / self.chunk_dim[0] / TILE_SIZE)) + ';' + str(math.floor(item.pos[1] / self.chunk_dim[1] / TILE_SIZE))
                    if not loc == target_chunk:
                      self.chunk_data[target_chunk].pop(i)
                      self.add_item(item)
        
    
