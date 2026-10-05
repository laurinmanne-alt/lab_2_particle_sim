from view import *
import math
import random

random.seed()

n = 10
particles = []
for i in range(n):
    pos = Vec(random.uniform(-8, 8), random.uniform(-8, 8))
    vel = Vec(random.uniform(-10, 10), random.uniform(-10, 10))
    mass = random.uniform(0.5, 3)
    particles.append(Particle(mass, pos, vel, 0.2*mass**0.5))


def no_force(dt,particles):
    pass

def forces(dt, particles):
    gravitational_force(dt, particles)
    circular_arena(dt, particles)

simulation_loop(forces, 0.000005, particles,)