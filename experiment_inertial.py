from view import *
import math
import random

random.seed()

n = 10
particles = []
for i in range(n):
    pos = Vec(random.uniform(-7, 7), random.uniform(-7, 7))
    vel = Vec(random.uniform(-7.5, 7.5), random.uniform(-7.5, 7.5))
    mass = random.uniform(0.5, 3)
    particles.append(Particle(mass, pos, vel, 0.2*mass**0.5))


def no_force(dt,particles):
    pass

def forces(dt, particles):
    gravitational_force(dt, particles)

simulation_loop(forces, 0.0001, particles,)