import pygame, json

class LeafSpawnLoader:
  def __init__(self, app, path='data/config/leaf.json'):
    self.path = path
    self.app = app

  def load(self, path):
    with open(path, 'r') as f:
      leaf_data = json.read(f)
      rect_data = {}
      for mode in leaf_data:
        for variant in leaf_data[mode]:
          data = leaf_data[mode][variant]
          rect_data[mode][variant] = pygame.Rect(data)
