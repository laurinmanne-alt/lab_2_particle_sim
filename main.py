"""Run the particle simulation.

Particles start at random positions with random velocities and masses.
They attract each other with gravity, bounce off each other, and stay
inside a circular arena.
"""

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
    # Radius grows with mass, so heavier particles look bigger
    particles.append(Particle(mass, pos, vel, 0.2*mass**0.5))


def forces(dt, particles):
    """Apply all forces for one time step."""
    collision(dt, particles)
    gravitational_force(dt, particles)
    circular_arena(dt, particles)


simulation_loop(forces, 0.00005, particles)
