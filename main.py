# Particles with gravity and collisions inside a circular arena.
# Start positions, velocities and masses are random.

from view import *
import math
import random
    
random.seed()

n = 10  # number of particles
particles = []
for i in range(n):
    pos = Vec(random.uniform(-7, 7), random.uniform(-7, 7))
    vel = Vec(random.uniform(-10, 10), random.uniform(-10, 10))
    mass = random.uniform(0.5, 3)
    particles.append(Particle(mass, pos, vel, 0.2*mass**0.5))  # heavier = bigger


def forces(dt, particles):
    collision(dt, particles)
    gravitational_force(dt, particles)
    circular_arena(dt, particles)


simulation_loop(forces, 0.00005, particles)
