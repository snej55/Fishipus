import pygame, math

from typing import TypeAlias
from .particles import KickUp, PhysicsParticles, Particle
from data.scripts.sword import Slash
from ..bip import *

ParticleList: TypeAlias = list[Particle]

class GFXManager:
    def __init__(self, app):
        self.sparks = []
        self.smoke = []
        self.impact = []
        self.shockwaves = []
        self.particle_systems = []
        self.shadows = []
        self.particle_systems = {}
        self.kick_up = []
        self.glow_dust = [] # totally best name ever lol
        self.slashs = []
        self.app = app
        self.particles = []
    
    def add_particle_system(self, name: str, mode: str, trail=None, friction=0.999, bounce=0.7, explode=None, gravity=0.24, fade=False, decay=0.005):
        if mode == 'kickup':
            self.particle_systems[name] = KickUp(self.app, friction, bounce, gravity, decay)
        elif mode == 'physics':
            self.particle_systems[name] = PhysicsParticles(self.app, trail, friction, bounce, explode, gravity, fade)
    
    def add_kickup(self, pos, vel, color, alpha, bounce=0.7, gravity=0.1, friction=0.999, decay=1, flags=0):
        self.kick_up.append([list(pos), list(vel), list(color), alpha, bounce, gravity, friction, None, decay, 0, flags])
    
    def add_glow_dust(self, pos, vel, color, alpha, bounce=0.7, gravity=0.1, friction=0.999, decay=1, flags=0):
        self.glow_dust.append([list(pos), list(vel), tuple(color), alpha, bounce, gravity, friction, color, decay, 0, flags])
    
    def add_smoke(self, pos, vel, scale, alpha, angle, target_angle, color):
        self.smoke.append([list(pos), list(vel), scale, alpha, angle, target_angle, color]) # [list(self.rect().center), [math.cos(angle) * speed, math.sin(angle) * speed], 1, random.randint(200, 255), 0, random.randint(0, 360), (200, 200, 255)]

    @staticmethod
    def alpha_surf(dim, alpha, color):
        surf = pygame.Surface(dim)
        surf.fill(color)
        surf.set_alpha(alpha)
        return surf.convert_alpha()
    
    def calc_smoke(self, smoke, scroll):
        smoke[0][0] += smoke[1][0] * self.app.dt
        smoke[0][1] += smoke[1][1] * self.app.dt
        smoke[1][0] += (smoke[1][0] * 0.98 - smoke[1][0]) * self.app.dt
        smoke[1][1] += (smoke[1][1] * 0.98 - smoke[1][1]) * self.app.dt
        smoke[4] += (smoke[5] - smoke[4]) / 2 * self.app.dt
        smoke[3] = max(0, smoke[3] - SMOKE_DELAY * self.app.dt)
        smoke[2] += 0.25 * self.app.dt
        surf = pygame.transform.rotate(self.alpha_surf([smoke[2], smoke[2]], smoke[3], smoke[6]), smoke[4])
        if not smoke[3]:
            self.smoke.remove(smoke)
        return (surf, (smoke[0][0] - surf.get_width() * 0.5 - scroll.x, smoke[0][1] - surf.get_height() * 0.5 - scroll.y))
    
    @staticmethod
    def circle_surf(radius, color):
        surf = pygame.Surface((radius*2, radius*2))
        pygame.draw.circle(surf, color, (radius, radius), radius)
        surf.set_colorkey((0, 0, 0))
        return surf
    
    def update_kickup(self, particle, scroll):
        if particle[9] < 10:
            particle[0][0] += particle[1][0] * self.app.dt
            if self.app.world.tile_map.physics_map.particle_solid(particle[0]):
                particle[1][0] *= -particle[4]
                particle[0][0] += particle[1][0] * self.app.dt * 2
                particle[1][1] *= particle[6]
            particle[0][1] += particle[1][1] * self.app.dt
            if self.app.world.tile_map.physics_map.particle_solid(particle[0]):
                particle[1][1] *= -particle[4]
                particle[0][1] += particle[1][1] * self.app.dt * 2
                particle[1][0] *= particle[6]
            if abs(particle[1][0]) < 0.03 and abs(particle[1][1]) < 0.03:
                particle[9] += 1 * self.app.dt
            particle[1][1] += particle[5] * self.app.dt
        for c in particle[2]:
            c = particle[3]
        if particle[0] in self.app:
            self.app.world.window.alpha_surf.set_at((particle[0][0] - scroll[0] - 0.5, particle[0][1] - scroll[1] - 0.5), particle[2])
        particle[3] -= particle[8] * self.app.dt
        if particle[3] < 1:
            return
        return 1
    def update(self, surf, scroll):
        for system in self.particle_systems:
            self.particle_systems[system].update(self.app.world.window.alpha_surf, scroll)
        for particle in self.particles.copy():
            kill = particle.update()
            if particle.particle_type == 'leaf' and (not particle.done):
                particle.pos[0] += math.sin(particle.frame * 0.08) * 0.8 * self.app.dt - 0.5 * self.app.dt
                particle.vel[1] = min(0.2, particle.vel[1] + 0.005 * self.app.dt)
            particle.draw(surf, scroll)
            if kill:
                self.particles.remove(particle)
        for spark in self.sparks.copy():
            kill = spark.update(self.app.dt)
            if not kill:
                spark.draw(surf, scroll)
            else:
                self.sparks.remove(spark)
        self.kick_up = [particle for particle in self.kick_up if self.update_kickup(particle, scroll)]
        for i, particle in sorted(enumerate(self.glow_dust.copy()), reverse=True): # [pos, vel, color, alpha, bounce, gravity, friction, color, decay=1]
            if particle[9] < 10:
                particle[0][0] += particle[1][0] * self.app.dt
                if self.app.world.tile_map.physics_map.particle_solid(particle[0]):
                    particle[1][0] *= -particle[4]
                    particle[0][0] += particle[1][0] * self.app.dt * 2
                    particle[1][1] *= particle[6]
                particle[0][1] += particle[1][1] * self.app.dt
                if self.app.world.tile_map.physics_map.particle_solid(particle[0]):
                    particle[1][1] *= -particle[4]
                    particle[0][1] += particle[1][1] * self.app.dt * 2
                    particle[1][0] *= particle[6]
                if abs(particle[1][0]) < 0.03 and abs(particle[1][1]) < 0.03:
                    particle[9] += 1 * self.app.dt
                particle[1][1] += particle[5] * self.app.dt
            if particle[0] in self.app:
                radius = particle[3] / 255 * 4
                self.app.world.window.alpha_surf.blit(self.circle_surf(radius, particle[7]), (particle[0][0] - radius * 0.5 - scroll[0] - 0.5, particle[0][1] - radius * 0.5 - scroll[1] - 0.5), special_flags=pygame.BLEND_RGBA_ADD)
                self.app.world.window.alpha_surf.set_at((particle[0][0] - scroll[0] - 0.5, particle[0][1] - scroll[1] - 0.5), (255, 255, 255))
            particle[3] -= particle[8] * self.app.dt
            if particle[3] < 50:
                self.glow_dust.pop(i)
        if len(self.glow_dust) > 300:
            self.glow_dust[0][3] = max(0, self.glow_dust[0][3] - 100)
        for impact in self.impact.copy():
            kill = impact.update(self.app.dt)
            if kill:
                self.impact.remove(impact)
            else:
                impact.draw(surf, scroll)
        for shadow in self.shadows.copy():
            shadow.draw(surf, scroll)
            if shadow.alpha < 1:
                self.shadows.remove(shadow)
        for slash in self.slashs.copy():
            slash.draw(surf, scroll)
            if slash.animation.finished:
                self.slashs.remove(slash)
        self.app.world.window.alpha_surf.fblits([self.calc_smoke(smoke, scroll) for smoke in self.smoke.copy()])
        for shockwave in self.shockwaves.copy():
            pygame.draw.circle(self.app.world.window.alpha_surf, shockwave[2], (shockwave[0][0] - scroll.x, shockwave[0][1] - scroll.y), min(shockwave[4] * 1.5, shockwave[1] * 1.5), int(math.ceil(max(1, shockwave[4] - shockwave[1]) / 4)))
            if shockwave[1] - 1 > shockwave[4]:
                if type(shockwave[2]) == tuple:
                    shockwave[2] = list(shockwave[2])
                shockwave[2][0] = max(shockwave[2][0] - 50 * self.app.dt, 0)
                shockwave[2][1] = max(shockwave[2][1] - 50 * self.app.dt, 0)
                shockwave[2][2] = max(shockwave[2][2] - 50 * self.app.dt, 0)
                if shockwave[2][2] == 0 and shockwave[2][1] == 0 and shockwave[2][0] == 0:
                    self.shockwaves.remove(shockwave)
            else:
                shockwave[1] += max(0, min(20, 150 * (shockwave[4] * 0.01) / max(0.0001, shockwave[1] * 2))) * self.app.dt * shockwave[3]
