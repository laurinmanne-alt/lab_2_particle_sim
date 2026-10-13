# Detta experiment testar bara gravitational_force(). Partiklarna kommer att starta på random ställen med random storlek, hastighet och massa. De kommer sedan påverkas av varandras gravitation och antagligen glida utanför skärmen. 
# När time-step ökas/minskas ökas eller minskas hastighten på simulationen. Eftersom mer tid hinner passera per iteration av main loopen och hastigheten av main loopen inte påverkas, kommer högre time-step reslutera i en snabbare simulaering och vice versa. 

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

def forces(dt, particles):
    gravitational_force(dt, particles)

simulation_loop(forces, 0.0001, particles)