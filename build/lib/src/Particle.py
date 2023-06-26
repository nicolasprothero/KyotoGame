import pygame

class Particle(pygame.sprite.Sprite):
    def __init__(self):
        self.particle_list = []

    def emit(self, screen):
        if self.particles:
            for particle in self.particles:
                particle[0] += -1
                particle[1] += -2
                particle[2] += -0.1
                pygame.draw.circle(screen, pygame.Color('White'), (particle[0], particle[1]), particle[2])

    def add_particles(self, x, y, radius):
        self.particle_list.append([x, y, radius])

    def delete_particles(self):
        particle_copy = [particle for particle in self.particle_list if particle[2] > 0]
        self.particle_list


