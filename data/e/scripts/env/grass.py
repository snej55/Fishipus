import pygame, gc, sys, random, math
from copy import deepcopy
from ..bip import *

class Grass:
    img_cache = {}
    def __init__(self, img, pos, tension, variant, tile_variant=0):
        self.img = img.copy()
        self.tile_variant = tile_variant
        self.img.convert()
        self.img.set_colorkey((0, 0, 0))
        self.img_copy = img.copy()
        self.pos = list(pos)
        self.angle = 0
        self.target_angle = 0
        self.angle_offset = math.sin(self.pos[0] * 5) * 20
        self.tension = tension
        self.variant = variant
        self.rect = pygame.Rect([self.pos[0] - 4, self.pos[1] + 2], [10, 10])
    
    def update_img(self, offset=1):
        key = (int(self.angle + self.angle_offset * offset), self.variant)
        if not key in self.img_cache:
            self.img_cache[key] = pygame.transform.rotate(self.img, key[0])
            self.img_cache[key].convert()
            self.img_cache[key].set_colorkey((0, 0, 0))
        self.img_copy = self.img_cache[key]
        return self.img_copy
    
    def update(self, wind, rect, dt):
        self.target_angle = wind
        if self.rect.colliderect(rect):
            distance = (rect.right - self.rect.centerx) ** 2 + (rect.centery - self.rect.centery) ** 2
            hd = rect.right - self.rect.centerx
            if distance < 1600:
                temp_target = 0
                if hd <= 0:
                    temp_target = -70 - hd * 3.5
                if hd > 0:
                    temp_target = 70 - hd * 3.5
                self.target_angle = min(self.target_angle + temp_target, 90)
                self.target_angle = max(self.target_angle, -90)
        self.angle += (self.target_angle - self.angle) / self.tension * dt
        self.angle = max(-90, min(self.angle, 90))
        self.update_img()
    
    def draw(self, dt, surf, scroll=(0, 0)):
        #pygame.draw.rect(surf, (255, 0, 0), self.rect, width=1)

        loc = (self.pos[0] + int(self.img.get_width() / 2) - int(self.img_copy.get_width() / 2) - scroll[0], self.pos[1] + int(self.img.get_height() / 2) - int(self.img_copy.get_height() / 2) - scroll[1])
        surf.blit(self.img_copy, loc)

class GrassTile:
    img_cache = {}
    def __init__(self, loc, variant, manager, tile_variant=0):
        self.loc = loc
        self.tile_variant = tile_variant
        self.pos = [int(coord) * TILE_SIZE for coord in loc.split(';')]
        self.grass = []
        self.variant = variant
        self.padding = 13
        self.default_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.default_surf.convert()
        self.default_surf.set_colorkey((0, 0, 0))
        self.updated = False
        self.manager = manager
        self.go_grass = False

    def wind(self):
        return max(-90, min(90, self.manager.wind(self.manager.app.time + math.sin(self.pos[0] * 0.5) * 25)))
    
    def update(self, rect, dt):
        for blade in self.grass:
            if not self.go_grass:
                blade.angle = self.wind()
            blade.update(self.wind(), rect, dt)
        self.updated = True
        self.go_grass = True
    
    def gen_assets(self, accuracy):
        img_surf = pygame.Surface((TILE_SIZE + self.padding * 2, TILE_SIZE + self.padding * 2))
        for i in range(-90, 91):
            key = (math.floor(i / accuracy), self.variant, self.tile_variant)
            if not (key in self.img_cache):
                img_surf.fill((0, 0, 0))
                blade_offset = deepcopy(self.grass[0].pos)
                for j, blade in enumerate(self.grass):
                    blade.angle = int(max(-90, min(90, i)))
                    blade.update_img()
                    loc = (self.padding + blade.pos[0] + int(blade.img.get_width() / 2) - int(blade.img_copy.get_width() / 2) - blade_offset[0], self.padding + blade.pos[1] + int(blade.img.get_height() / 2) - int(blade.img_copy.get_height() / 2) - blade_offset[1])
                    img_surf.blit(blade.img_copy, deepcopy(loc))
                img_surf.convert()
                img_surf.set_colorkey((0, 0, 0))
                self.img_cache[key] = img_surf.copy()
    
    def get_img(self, variant, angle, accuracy=2):
        key = (math.floor(angle / accuracy), variant, self.tile_variant)
        if key in self.img_cache:
            return self.img_cache[key]
        return self.default_surf

    def draw(self, dt, surf, scroll=(0, 0)):
        if self.updated:
            for blade in self.grass:
                blade.draw(dt, surf, (scroll[0], scroll[1]))
                if not self.updated:
                    blade.target_angle = self.wind()
        else:
            surf.blit(self.get_img(self.variant, self.wind(), GRASS_ACCURACY), (self.pos[0] - self.padding - scroll[0], self.pos[1] - self.padding - scroll[1]))
        if not self.updated:
            self.go_grass = False
        self.updated = False

class GrassAssets:
    def __init__(self, app, manager):
        self.app = app
        self.manager = manager
        self.assets = {}
        self.default_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.default_surf.convert()
        self.default_surf.set_colorkey((0, 0, 0))
    
    def get_img(self, variant, angle, accuracy=2):
        key = (math.floor(angle / accuracy), variant)
        if key in self.assets:
            return self.assets[key]
        return self.default_surf

class GrassManager:
    def __init__(self, app, grass_imgs):
        self.grass_assets = GrassAssets(app, self)
        self.grass_imgs = grass_imgs
        self.app = app
    
    def load(self, grass, amount, density):
        self.grass = self.load_grass(grass, amount, density)
        self.gen_assets(GRASS_ACCURACY)

    def gen_grass(self, grass_map, amount, density):
        grass = {}
        grass_order = [[random.randint(0, len(self.grass_imgs) - 1) for _ in range(len(self.grass_imgs))] for _ in range(8)]
        for loc in grass_map:
            grass[loc] = []
            pos = [int(coord) * TILE_SIZE for coord in loc.split(';')]
            tile_variant = random.randint(0, len(grass_order) - 1)
            for i in range(amount):
                aloc = [pos[0] + i * density, pos[1]]
                grass[loc].append(Grass(self.grass_imgs[grass_order[tile_variant][i % len(grass_order)]], aloc, GRASS_TENSION, grass_order[tile_variant][i % len(grass_order)], tile_variant=tile_variant))
        return grass

    def load_grass(self, grass, amount, density):
        grass_map = {}
        # group grass
        grass = self.gen_grass(grass, amount, density)
        for loc in grass:
            if not loc in grass_map:
                grass_map[loc] = GrassTile(loc, grass[loc][0].variant, self, tile_variant=grass[loc][0].tile_variant)
            grass_map[loc].grass.extend(grass[loc])
        # load tile cache
        # angle range is -90 <-> 90
        return grass_map
    
    def gen_assets(self, accuracy):
        for loc in self.grass:
            self.grass[loc].gen_assets(accuracy)
    
    def get_grass_tiles(self, pos):
        tiles = []
        tile_loc = (math.floor(pos[0] / TILE_SIZE), math.floor(pos[1] / TILE_SIZE))
        for offset in NEIGHBOUR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.grass:
                tiles.append(self.grass[check_loc])
        return tiles

    def update(self, rects):
        for rect in rects:
            for tile in self.get_grass_tiles(rect.center):
                tile.update(rect, self.app.dt)
    
    @staticmethod
    def wind(time):
        wind = math.sin(time * 0.05) * 30 + math.sin(time * 0.1) * 5 + math.cos(time * 0.3) * 10 + abs(math.sin(time * 0.2)) * 20 + 30
        wind += (0 - wind) * 0.6
        return wind
    
    def draw(self, surf, scroll=(0, 0)):
        for x in range(math.floor(scroll[0] / TILE_SIZE), math.floor((scroll[0] + surf.get_width()) / TILE_SIZE + 2)):
            for y in range(math.floor(scroll[1] / TILE_SIZE), math.floor((scroll[1] + surf.get_height()) / TILE_SIZE + 2)):
                loc = str(x - 1) + ';' + str(y - 1)
                if loc in self.grass:
                    self.grass[loc].draw(self.app.dt, surf, scroll)
