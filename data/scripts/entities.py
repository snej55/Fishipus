import pygame, math, random

from data.e.scripts.entities.ents import Entity, PlayerBase
from data.e.scripts.gfx.particles import Particle
from data.e.scripts.gfx.sparks import Spark
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
    
    def die(self):
        self.app.world.tick.slomo = 0.01
        self.app.world.window.camera.screen_shake = max(self.app.world.window.camera.screen_shake, 8)
        self.state = 'idle'
        palette = self.palette()
        for _ in range(random.randint(10, 20)):
            angle = random.random() * math.pi * 2
            speed = random.random() * 5
            self.app.world.gfx_manager.particles.append(Particle(self.app, 'particle', self.rect().center, [math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], random.randint(0, 7)))
            self.app.world.gfx_manager.particle_systems['cinders'].append([list((self.rect().centerx, self.rect().bottom)), [math.cos(angle) * speed, math.sin(angle) * speed], random.randint(2, 20), (230, 215, 204)])
        for _ in range(random.randint(10, 20)):
            angle = random.random() * math.pi * 2
            self.app.world.gfx_manager.sparks.append(Spark(self.rect().center, angle, random.random() + 2, (255, 255, 255), scale=0.5, decay=0.02))
        for _ in range(random.randint(120, 150)):
            angle = random.random() * math.pi * 2
            vel = random.random() * 2 + 2
            self.app.world.gfx_manager.add_kickup(self.rect().center, (math.cos(angle) * vel * 0.25, math.sin(angle) * vel * 2), random.choice(palette), random.randint(100, 200), friction=0.95, flags=pygame.BLEND_RGBA_ADD)
        self.app.world.gfx_manager.shockwaves.append([list(self.rect().center), 0.01, (230, 215, 204), 1.2, 25])
    
    def update(self):
        if not self.hit:
            if self.collide_mask(self.app.player.sword.attack_mask, self.app.player.sword.attack_offset):
                self.damage()
                self.app.world.window.camera.screen_shake = max(self.app.world.window.camera.screen_shake, 2)
                self.hit = True
                self.app.world.tick.slomo = 0.6
                state = self.state
                self.state = 'idle'
                palette = self.palette()
                self.state = state
                for _ in range(random.randint(5, 15)):
                    angle = random.random() * math.pi * 2
                    vel = random.random() * 2 + 2
                    self.app.world.gfx_manager.add_kickup(self.rect().center, (math.cos(angle) * vel, math.sin(angle) * vel), random.choice(palette), random.randint(100, 200), friction=0.95)
        elif not self.collide_mask(self.app.player.sword.attack_mask, self.app.player.sword.attack_offset):
            self.hit = False
        return super().update()
    
    def handle_animations(self):
        self.state = 'idle'
        self.frames['idle'] = self.anim['idle'].update(self.app.dt)
        return super().handle_animations()
        
    