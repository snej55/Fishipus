import pygame, math, random

from ..gfx.particles import Particle
from ..gfx.anim import Animation
from ..bip import *

class EntityManager:
    def __init__(self, app):
        self.app = app
        self.ents_frame = {}
        self.entities_updated = 0
        self.entity_rects = []
    
    def get_quad(self, pos):
        loc = str(int(pos[0] / TILE_SIZE / ENTITY_QUAD_SIZE[0])) + ';' + str(int(pos[1] / TILE_SIZE / ENTITY_QUAD_SIZE[1]))
        if not loc in self.ents_frame:
            self.ents_frame[loc] = []
        return self.ents_frame[loc]
    
    def update(self, surf, scroll):
        self.entities_updated = 0
        self.entity_rects = []
        for y in range(math.ceil(surf.get_height() / (ENTITY_QUAD_SIZE[1] * TILE_SIZE)) + 2):
            for x in range(math.ceil(surf.get_width() / (ENTITY_QUAD_SIZE[0] * TILE_SIZE)) + 2):
                target_x = x - 2 + math.ceil(int(scroll[0]) / (ENTITY_QUAD_SIZE[0] * TILE_SIZE))
                target_y = y - 2 + math.ceil(int(scroll[1]) / (ENTITY_QUAD_SIZE[1] * TILE_SIZE))
                target_quad = f'{target_x};{target_y}'
                if target_quad in self.ents_frame:
                    for i, entity in sorted(enumerate(self.ents_frame[target_quad]), reverse=True):
                        kill = entity.update()
                        entity.draw(surf, scroll)
                        self.entities_updated += 1
                        self.entity_rects.append(entity.rect())
                        if kill:
                            entity.die()
                            self.ents_frame[target_quad].pop(i)
                            del entity
                        elif not self.get_quad(entity.pos) is entity.quad:
                            self.get_quad(entity.pos).append(entity)
                            self.ents_frame[target_quad].pop(i)
        self.entity_rects.append(self.app.player.rect())

#  Entity parent class
class Entity:
    def __init__(self, pos, dimensions, anim_offset, app, e_type, fiend=True, enemy=None, mask_collide_offset=None, hurt_recovery=1, hurt_flash=5, health=10):
        self.pos = pygame.Vector2(pos)
        self.dimensions = pygame.Vector2(dimensions)
        self.anim_offset = pygame.Vector2(anim_offset)
        self.fiend = fiend
        self.enemy = enemy
        self.app = app
        self.mode = e_type
        self.state = 'idle'
        self.frames = {'idle': 0, 'run': 0}
        self.movement = pygame.Vector2(0, 0)
        self.collisions = {'left': False, 'right': False, 'up': False, 'down': False}
        self.flipped = False
        self.hurt_recovery = hurt_recovery
        self.hurt_flash = hurt_flash
        self.orig_anim_offset = pygame.Vector2(anim_offset)
        self.hit = False
        self.gravity = 0.3
        self.outside = pygame.Vector2(0, 0)
        self.health = health
        self.platmode_collided = False
        self.falling = 99
        self.controls = {'up': False}
        self.hurt = 99
        self.name = type(self).__name__
        if self.mode != 'player':
            self.quad = self.app.world.entity_manager.get_quad(self.pos)
            self.quad.append(self)
        
    def collide_mask(self, mask, pos):
        offset = (pos[0] - self.pos.x, pos[1] - self.pos.y)
        return self.hurt_mask.overlap(mask, offset)
    
    def distance_to(self, entity):
        return self.pos.distance_to(entity.pos)
    
    def __getitem__(self, item):
        return self.__dict__[item]
    
    def die(self):
        pass
    
    def get_colliding_ents(self, rect=None):
        entity_rect = rect if rect else self.rect()
        entities = []
        for y in range(3):
            for x in range(3):
                loc = str(int(self.pos[0] / TILE_SIZE / ENTITY_QUAD_SIZE[0]) + x - 1) + ';' + str(int(self.pos[1] / TILE_SIZE / ENTITY_QUAD_SIZE[1]) + y - 1)
                if loc in self.app.entity_manager.ents_frame:
                    for entity in self.app.entity_manager.ents_frame[loc]:
                        if entity.rect().colliderect(entity_rect):
                            entities.append(entity)
        return entities
    
    def get_neighbours(self):
        for y in range(3):
            for x in range(3):
                loc = str(int(self.pos[0] / TILE_SIZE / ENTITY_QUAD_SIZE[0]) + x - 1) + ';' + str(int(self.pos[1] / TILE_SIZE / ENTITY_QUAD_SIZE[1]) + y - 1)
                if loc in self.app.entity_manager.ents_frame:
                    for entity in self.app.entity_manager.ents_frame[loc]:
                        yield entity

    def copy(self):
        entity = Entity(self.pos, self.dimensions, self.anim_offset, self.app, self.mode, self.fiend, self.enemy)
        entity.__dict__ = dict(self.__dict__)
        entity.quad = self.app.entity_manager.get_quad(self.pos)
        return entity

    def chk(self, attr, val=None):
        if not hasattr(self, attr):
            setattr(self, attr, val)
        return getattr(self, attr)
    
    def palette(self):
        return self.app.palettes[self.mode + '/' + self.state][math.floor(self.frames[self.state] % len(self.animation()))][0]

    def sec(self):
        self.chk('collisions', {'left': False, 'right': False, 'up': False, 'down': False})
        self.chk('state', 'idle')
        self.chk('mode')
        self.chk('pos')
        self.frames['hurt'] = 0
        self.hurt_mask = pygame.mask.from_surface(self.img().copy())
        hurt_surf = pygame.Surface(self.hurt_mask.get_size())
        hurt_surf.blit(self.hurt_mask.to_surface(), (0, 0))
        hurt_surf = pygame.transform.scale(hurt_surf, (hurt_surf.get_width() + 2, hurt_surf.get_height() + 2))
        hurt_surf.set_colorkey((0, 0, 0))
        self.app.assets['game'][self.mode + '/' + 'hurt'] = [hurt_surf]
    
    def rect(self):
        return pygame.Rect(self.pos.x, self.pos.y, self.dimensions.x, self.dimensions.y)

    def handle_animations(self):
        self.hurt += self.hurt_recovery * self.app.dt
        self.anim_offset = pygame.Vector2(self.orig_anim_offset)
        if self.hurt < self.hurt_flash:
            self.state = 'hurt'
            self.anim_offset = pygame.Vector2(self.orig_anim_offset[0] - 1, self.orig_anim_offset[1] - 1)
            self.frames['hurt'] = 0
            return self.hurt
        return None
    
    def update(self):
        if self.movement.y > 4:  # terminal velocity
            self.movement.y = 4
        frame_movement = pygame.Vector2(self.movement.x + self.outside.x, self.movement.y + self.outside.y)

        self.pos.x += frame_movement.x * self.app.dt
        self.falling += 1 * self.app.dt
        self.collisions = {'left': False, 'right': False, 'up': False, 'down': False}
        entity_rect = self.rect()
        for rect in self.app.world.tile_map.physics_map.physics_rects_around(self.pos):
            if rect.colliderect(entity_rect):
                if frame_movement.x * self.app.dt > 0:
                    self.collisions['right'] = True
                    entity_rect.right = rect.left
                if frame_movement.x * self.app.dt < 0:
                    self.collisions['left'] = True
                    entity_rect.left = rect.right
                self.pos.x = entity_rect.x
        self.pos.y += frame_movement.y * self.app.dt
        entity_rect = self.rect()
        for rect in self.app.world.tile_map.physics_map.physics_rects_around(self.pos):
            if rect.colliderect(entity_rect):
                if frame_movement.y * self.app.dt > 0:
                    self.collisions['down'] = True
                    entity_rect.bottom = rect.top
                    self.falling = 0
                if frame_movement.y * self.app.dt < 0:
                    self.collisions['up'] = True
                    entity_rect.top = rect.bottom
                self.movement.y = 0
                self.outside.y = 0
                self.pos.y = entity_rect.y

        self.movement.y = min(16, self.movement.y + self.gravity * self.app.dt)
        return self.health < 0 or self.app.world.tile_map.physics_map.tile_type_at(self.rect().center) in self.app.danger

    def damage(self, intt=1):
        self.health -= intt
        self.hurt = 0

    def animation(self, mode=None):
        return self.app.assets['game'][type(self).__name__.lower() + '/' + (mode if mode else self.state)]

    def img(self) -> pygame.Surface:
        return pygame.transform.flip(self.animation()[math.floor(self.frames[self.state] % len(self.animation()))], self.flipped, False)

    def draw(self, surf, scroll=(0, 0)):
        self.handle_animations()
        surf.blit(self.img(), (self.pos.x - int(scroll.x) + self.anim_offset.x, self.pos.y - int(scroll.y) + self.anim_offset.y))

inAir = lambda entity: entity.falling > entity.fall_buff
xMotion = lambda entity: abs(entity.movement[0]) > 0.025
grounded = lambda entity: entity.grounded < entity.ground_buff

# TODO: MAKE A SWORD FOR THIS DUDE!!
class PlayerBase(Entity):
    def __init__(self, pos, dimensions, anim_offset, app, air_friction=0.56, friction=0.54, vx=1.4, vj=-3.15, jump_buff=15, double_jump=1, gravity_apr=[0.16,0.32,0.1,1,0], out_dim=0.5,
             grounded_tim=1, jump_tim=1, fall_buff=12, ground_buff=20, jump_animbuff=200):
        super().__init__(pos, dimensions, anim_offset, app, 'player', False, 'all')
        self.controls = {'up': False, 'down': False, 'left': False, 'right': False}
        self.frames = {'idle': 0, 'jump': 0, 'run': 0, 'land': 0}
        self.anim = {'idle': Animation(self, self.animation(mode='idle'), 0.2, True),
                     'jump': Animation(self, self.animation(mode='jump'), 0.4, False, indep=['falling', jump_animbuff]),
                     'run': Animation(self, self.animation(mode='run'), 0.4, True),
                     'land': Animation(self, self.animation(mode='land'), 0.125, False, indep=['grounded', ground_buff])}
        self.jumping = 99
        self.ground_buff = ground_buff
        self.double_jump = 1
        self.grounded = 0
        self.friction = friction
        self.air_friction = air_friction
        self.vx = vx
        self.jump_buff = jump_buff
        self.jumps = 0
        self.double_jump = double_jump
        self.vj = vj
        self.gravity_apr = list(gravity_apr)
        self.out_dim = out_dim
        self.grounded_tim = grounded_tim
        self.jump_tim = jump_tim
        self.fall_buff = fall_buff
        self.jumped = 99
        self.sec()

    def update(self):
        self.grounded += self.grounded_tim * self.app.dt
        self.jumping += self.jump_tim * self.app.dt
        self.controls = {'up': self.controls['up'], 'down': self.app.keys[pygame.K_DOWN] or self.app.keys[pygame.K_s], 'left': self.app.keys[pygame.K_LEFT] or self.app.keys[pygame.K_a], 'right': self.app.keys[pygame.K_RIGHT] or self.app.keys[pygame.K_d]}
        if self.controls['left']:
            self.movement[0] -= self.vx
            self.flipped = True
        if self.controls['right']:
            self.movement[0] += self.vx
            self.flipped = False
        if (self.app.keys[pygame.K_UP] or self.app.keys[pygame.K_w]):
            self.controls['up'] = True
            self.jumping = 0
        else:
            self.controls['up'] = False
        if pygame.K_UP in self.app.toggles and self.falling < self.fall_buff and self.controls['up']:
            self.jumped = 1
        if self.jumped <= 6 and self.controls['up']:
            self.movement[1] = max(self.vj, min(-0.2, self.vj * 0.65))
        else:
            self.jumped = 7
        self.jumped += 0.5 * self.app.dt
        if not (self.falling > self.fall_buff and (self.controls['left'] or self.controls['right'])):
            self.movement[0] *= self.air_friction
        else:
            self.movement[0] *= self.friction
        if self.falling < self.fall_buff:
            self.jumps = 0
        if not self.jumps:
            if self.falling >= self.fall_buff:
                self.jumps = 1
        if self.movement[1] ** 2 < self.gravity_apr[3]:
            self.gravity = self.gravity_apr[0]
        else:
            self.gravity = self.gravity_apr[1]
        if self.movement[1] > self.gravity_apr[4]:
            self.gravity += self.gravity_apr[2]
        self.outside[0] = min(self.outside[0] + self.out_dim * self.app.dt, 0) if self.outside[0] else max(self.outside[0] - self.out_dim * self.app.dt, 0)
        self.outside[1] = min(self.outside[1] + self.out_dim * self.app.dt, 0) if self.outside[1] < 0 else max(self.outside[1] - self.out_dim * self.app.dt, 0)
        return super().update()

    def handle_animations(self):
        if self.falling >= self.fall_buff:
            self.state = 'jump'
            self.grounded = 0
            self.frames['idle'] = 1
            self.frames['jump'] = self.anim['jump'].update(self.app.dt)
        elif round(self.movement[0]):
            self.state = 'run'
            self.frames['run'] = self.anim['run'].update(self.app.dt)
            self.frames['idle'] = 1
        elif self.grounded < self.ground_buff:
            self.state = 'land'
            self.frames['land'] = self.anim['land'].update(self.app.dt)
            self.frames['idle'] = 1
        else:
            self.state = 'idle'
            self.frames['idle'] = self.anim['idle'].update(self.app.dt)
            self.frames['run'] = 7
        return super().handle_animations()
