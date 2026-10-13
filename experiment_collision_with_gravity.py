# Detta experiment visar funktionerna collision(), gravitational_force() och circular_arena(). Partiklarna borde dras mot varandra tack vare gravitational_force(), studsa på varandra med collision() och ha en cirkulär arena/bana där partiklarna studsar på väggen. 
# Experimentet funkar som väntat. Partiklarna rör sig genom väggen något innan de vänder och studsar tillbaka, men det är väntat då circular_arena() skapar en kraft på partiklarna och det därför tar lite tid för dem att bromsa in och sedan accelerera åt andra hållet. 

from view import *
import math
import random

random.seed()

n = 10
particles = []
for i in range(n):
    pos = Vec(random.uniform(-7, 7), random.uniform(-7, 7))
    vel = Vec(random.uniform(-10, 10), random.uniform(-10, 10))
    mass = random.uniform(0.5, 3)
    particles.append(Particle(mass, pos, vel, 0.2*mass**0.5))


def forces(dt, particles):
    collision(dt, particles)
    gravitational_force(dt, particles)
    circular_arena(dt, particles, canvas, to_canvas_coords)

simulation_loop(forces, 0.00005, particles)