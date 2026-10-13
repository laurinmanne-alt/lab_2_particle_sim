#   Detta experiment testar gravitationsfält tillsammans med kollisioner. Vi har också använt wall_force 
#   så att partiklarna ska hålla sig inuti fönstret

from view import *
import math
import random

random.seed()

n = 10
particles = []
for i in range(n):
    pos = Vec(random.uniform(-7, 7), random.uniform(-7, 7))
    vel = Vec(random.uniform(-5, 5), random.uniform(-2, 2))
    mass = random.uniform(1, 4)
    particles.append(Particle(mass, pos, vel, 0.2*mass**0.5))

# particles.append(Particle(5, Vec(0,0), Vec(1,0), 0.2*5**0.5))
# particles.append(Particle(4, Vec(3,0), Vec(-2,0), 0.2*4**0.5))

def combined_walls(dt, particles):
    wall_force(dt, particles, 1000, Vec(0,1), Vec(0,-9))
    wall_force(dt, particles, 1000, Vec(-1,0), Vec(11,0))
    wall_force(dt, particles, 1000, Vec(1,0), Vec(-11,0))
    wall_force(dt, particles, 1000, Vec(0,-1), Vec(0,10))

def forces(dt, particles):
    collision(dt, particles)
    combined_walls(dt, particles)
    constant_gravitational_field(dt, particles)

simulation_loop(forces, 0.0001, particles,)