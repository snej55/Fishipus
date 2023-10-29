import pygame

from typing import TypeAlias
from data.e.scripts.gfx.particles import KickUp, PhysicsParticles, Particle
from data.scripts.sword import Slash

ParticleList: TypeAlias = list[Particle]

class GFXManager:
    def __init__(self, app):
        self.sparks = []
        self.smoke = []
        self.impact = []
        self.shockwaves = []
        self.particles = []
        self.shadows = []
        self.particle_systems = {}
        self.slashs = []
        self.app = app
    
    def add_particle_system(self, name: str, mode: str, trail=None, friction=0.999, bounce=0.7, explode=None, gravity=0.24, fade=False, decay=0.005):
        if mode == 'kickup':
            self.particle_systems[name] = KickUp(self.app, friction, bounce, gravity, decay)
        elif mode == 'physics':
            self.particle_systems[name] = PhysicsParticles(self.app, trail, friction, bounce, explode, gravity, fade)

    @staticmethod
    def alpha_surf(dim, alpha, color):
        surf = pygame.Surface(dim)
        surf.fill(color)
        surf.set_alpha(alpha)
        return surf.convert_alpha()
    
    def calc_smoke(self, smoke, scroll):
        smoke[0][0] += smoke[1][0] * self.dt
        smoke[0][1] += smoke[1][1] * self.dt
        smoke[1][0] += (smoke[1][0] * 0.98 - smoke[1][0]) * self.dt
        smoke[1][1] += (smoke[1][1] * 0.98 - smoke[1][1]) * self.dt
        smoke[4] += (smoke[5] - smoke[4]) / 2 * self.dt
        smoke[3] = max(0, smoke[3] - SMOKE_DELAY * self.dt)
        smoke[2] += 0.2 * self.dt
        surf = pygame.transform.rotate(self.alpha_surf([smoke[2], smoke[2]], smoke[3], smoke[6]), smoke[4])
        if not smoke[3]:
            self.smoke.remove(smoke)
        return (surf, (smoke[0][0] - surf.get_width() * 0.5 - scroll.x, smoke[0][1] - surf.get_height() * 0.5 - scroll.y))
    
    def update(self, surf, scroll):
        for system in self.particle_systems:
            self.particle_systems[system].update(surf, scroll)
        for spark in self.sparks.copy():
            kill = spark.update(self.app.dt)
            if not kill:
                spark.draw(surf, scroll)
            else:
                self.sparks.remove(spark)
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
        surf.fblits([self.calc_smoke(smoke) for smoke in self.smoke.copy()])
        for shockwave in self.shockwaves.copy():
            pygame.draw.circle(surf, shockwave[2], (shockwave[0][0] - scroll.x, shockwave[0][1] - scroll.y), min(shockwave[4] * 1.5, shockwave[1] * 1.5), int(math.ceil(max(1, shockwave[4] - shockwave[1]) / 4)))
            if shockwave[1] - 1 > shockwave[4]:
                self.shockwaves.remove(shockwave)
            else:
                shockwave[1] += max(0, min(20, 150 * (shockwave[4] * 0.01) / max(0.0001, shockwave[1] * 2))) * self.app.dt * shockwave[3]
