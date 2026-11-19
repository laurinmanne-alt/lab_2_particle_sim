import math


class Vec:
    """2D vector for positions, velocities and forces. Works with +, - and * (with a number)."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __mul__(self, factor):
        return Vec(factor*self.x, factor*self.y)

    # so that 2 * v works, not just v * 2
    def __rmul__(self, factor):
        return Vec(self.x*factor, self.y*factor)

    def __add__(self, other):
        return Vec(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Vec(self.x-other.x, self.y-other.y)

    def norm(self):
        """Length of the vector."""
        return math.sqrt(self.x**2 + self.y**2)

    def get_coords(self):
        return (self.x, self.y)


class Particle:
    """A round particle with mass, position, velocity and radius."""

    def __init__(self, mass, position, velocity, radius):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.radius = radius

    def inertial_move(self, dt):
        """Move the particle one step with its current velocity."""
        self.position = dt*self.velocity + self.position

    def apply_force(self, dt, f):
        """Apply force f for time dt. Only changes the velocity."""
        a = 1/self.mass*f
        self.velocity = dt*a + self.velocity

    def bounding_box(self):
        """Top-left and bottom-right corner of the box around the particle (used for drawing)."""
        top_left = Vec(self.position.get_coords()[0]-self.radius, self.position.get_coords()[1]+self.radius)
        bottom_right = Vec(self.position.get_coords()[0]+self.radius, self.position.get_coords()[1]-self.radius)

        return top_left, bottom_right


def dot(u, v):
    """Dot product of two vectors."""
    return u.x*v.x + u.y*v.y


def constant_gravitational_field(dt, particles, g=10):
    """Pulls all particles straight down. g is the acceleration (about 10 on earth)."""
    for p in particles:
        f = g*p.mass*Vec(0,-1)
        p.apply_force(dt, f)


def circular_arena(dt, particles, k=10000, R=9):
    """Keeps the particles inside a circle with radius R.

    If a particle goes outside it gets pushed back in. k decides how hard the wall is.
    """
    for p in particles:
        r = p.position.norm()
        if R < r:
            f = k * (R - r) * (p.position * (1/r))
            p.apply_force(dt, f)


def wall_force(dt, particles, k, n, a):
    """A straight wall that particles bounce off.

    a is a point on the wall and n is the normal, pointing inwards.
    k decides how hard the wall is.
    """
    for p in particles:
        d = dot((p.position-a), n)
        f = -d*k*n
        if d < 0:
            p.apply_force(dt, f)


def gravitational_force(dt, particles, G=15):
    forces = [Vec(0, 0) for p in particles]
    
    for i in range(len(particles) - 1):
        for j in range(i + 1, len(particles)):
            p1 = particles[i]
            p2 = particles[j]
            diff = p2.position - p1.position
            r = diff.norm()
            # skip if they overlap, otherwise r gets close to 0 and the force blows up
            if r <= p2.radius + p1.radius:
                continue

            F = G * p2.mass * p1.mass / r**2
            f2 = (F / r) * diff
            forces[i] += f2
            forces[j] -= f2

    for x in range(len(particles)):
        particles[x].apply_force(dt, forces[x])


def collision(dt, particles, k=1000000):
    """Pushes overlapping particles apart. The more they overlap, the harder the push."""
    for p2 in particles:
        total_force = Vec(0, 0)
        for p1 in particles:
            if p1 is not p2:
                r = (p2.position-p1.position).norm()
                if r < (p2.radius + p1.radius):
                    force_magnitude = k*(p2.radius + p1.radius - r)
                    force_direction = p2.position-p1.position
                    total_force = total_force + force_magnitude*(1/(force_direction.norm()))*force_direction
        p2.apply_force(dt, total_force)
