import math

# Task (2/12): Define a class Vec
class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __mul__(self, factor):
        return Vec(factor*self.x, factor*self.y)

    def __rmul__(self, factor):
        return Vec(self.x*factor, self.y*factor)

    def __add__(self, other):
        return Vec(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Vec(self.x-other.x, self.y-other.y)

    def norm(self):
        return math.sqrt(self.x**2 + self.y**2)

    def get_coords(self):
        return (self.x, self.y)

# Task (3/12): Additionally define a function dot(u, v)
def dot(u, v):
    return u.x*v.x + u.y*v.y

# Task (4/12): Create a class Particle
class Particle:
    def __init__(self, m, x, v, r):
        self.mass = m
        self.position = x
        self.velocity = v
        self.radius = r

# Task (5/12): In the Particle class, implement a method inertial_move(self, dt).
    def inertial_move(self, dt):
        self.position = dt*self.velocity + self.position

# Task (6/12): In the Particle class, implement a method apply_force(self, dt, f)
    def apply_force(self, dt, f):
        a = 1/self.mass*f
        self.velocity = dt*a + self.velocity

# Task (9/12): In the Particle class, add a method bounding_box(self)
    def bounding_box(self):
        top_left = (self.position.get_coords()[0]-self.radius, self.position.get_coords()[1]+self.radius)
        bottom_right = (self.position.get_coords()[0]+self.radius, self.position.get_coords()[1]-self.radius)

        return top_left, bottom_right

##########################################
### NB. Tasks 7–8 are done in view.py. ###
##########################################


###########################################
### When you're done with all 12 tasks: ###
### forces/other features in this file! ###
###########################################

def constant_gravitational_field(dt, particles, g=10):
    for p in particles:
        f = g*p.mass*Vec(0,-1)
        p.apply_force(dt, f)

def circular_arena(dt, particles, k=100000, R=9):
    for p in particles:
        r = p.position.norm()
        if R < r:
            f = k * (R - r) * (p.position * (1/r))
            p.apply_force(dt, f)

def gravitational_force(dt, particles, G=500):
    for p in particles:
        total = Vec(0, 0)


        for other in particles:
            if other is not p: 
                diff = other.position - p.position
                r = diff.norm()
                if r <= p.radius + other.radius:
                    continue

                F = G * p.mass * other.mass / r**2
                f2 = (F / r) * diff
                total += f2

        p.apply_force(dt, total)
def collision(dt, particles, k):
    for p2 in particles:
        total_force = Vec(0, 0)
        for p1 in particles:
            if p1 is not p2:
                r = (p2.position-p1.position).norm()
                if r < (p2.radius + p1.radius):
                    force_magnitude = k*(p2.radius + p1.radius - r)
                    total_force = total_force + force_magnitude*(p2.position-p1.position)
                    # print(total_force)
        p2.apply_force(dt, total_force)
