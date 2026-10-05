from view import *
import math


u1 = Vec(0, 1)
u2 = Vec(0, -1)

# particles = [Particle(1, u1, u2, 0.3), Particle(1, u2, u1, 0.3)]
particles = []

n = 20
for i in range(n):
    theta = i*2*math.pi/n
    u = Vec(math.cos(theta),math.sin(theta))
    pos = 10 * u
    vel = -1 * u 
    particles.append(Particle(1,pos,vel,0.2))

def force(dt, particles):
    collision(dt, particles, 10000)

simulation_loop(force, 0.0005, particles)