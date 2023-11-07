import pygame, math, random

from data.e.scripts.entities.ents import Entity, PlayerBase
from data.scripts.sword import Sword
from data.e.scripts.gfx.anim import Animation

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

class Blobbo(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frames = {'idle': 0}
        self.anim = {'idle': Animation(self, self.app.assets['game']['blobbo/idle'], 0.25, True)}
        self.sec()
    
    def update(self):
        if self.collide_mask(self.app.player.sword.attack_mask, self.app.player.sword.attack_offset) and not self.hit:
            self.hurt = 4
            self.app.world.window.camera.screen_shake = max(self.app.world.window.camera.screen_shake, 2)
            self.hit = True
            self.app.world.tick.slomo = 0.5
            for _ in range(random.randint(5, 15)):
                angle = random.random() * math.pi * 2
                vel = random.random() * 2 + 2
                self.app.world.gfx_manager.particles['kick_up'].spawn(self.rect().center, (math.cos(angle) * vel, math.sin(angle) * vel), random.choice([(5, 50, 57), (0, 95, 65), (8, 178, 59), (71, 246, 65)]), random.randint(100, 200))
        else:
            self.hit = False
        return super().update()
    
    def handle_animations(self):
        self.state = 'idle'
        self.frames['idle'] = self.anim['idle'].update(self.app.dt)
        return super().handle_animations()
        
    