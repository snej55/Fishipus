import pygame, math

from data.e.scripts.entities.ents import Entity, PlayerBase
from data.scripts.sword import Sword

class Player(PlayerBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sword = Sword(self.app, self.pos, self, offset=(-1, -6))
    
    def update(self, *args):
        if (pygame.K_x in self.app.toggles or pygame.K_z in self.app.toggles)and self.sword.attacked > 10:
            self.sword.attack()
        self.sword.update()
        return super().update(*args)
    
    def draw(self, surf, scroll=(0, 0)):
        if self.sword.target_dir == -math.pi * 0.25:
            self.sword.draw(surf, scroll)
            return super().draw(surf, scroll)
        super().draw(surf, scroll)
        self.sword.draw(surf, scroll)

        
    