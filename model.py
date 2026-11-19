import math


class Vec:
    """A 2D vector, used for positions, velocities and forces.

    Supports + and - with another Vec, and * with a number
    (in either order: v * 2 or 2 * v).
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __mul__(self, factor):
        return Vec(factor*self.x, factor*self.y)

    # Lets the number come first: 2 * v, not only v * 2
    def __rmul__(self, factor):
        return Vec(self.x*factor, self.y*factor)

    def __add__(self, other):
        return Vec(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Vec(self.x-other.x, self.y-other.y)

    def norm(self):
        """Return the length of the vector."""
        return math.sqrt(self.x**2 + self.y**2)

    def get_coords(self):
        """Return (x, y) as a tuple."""
        return (self.x, self.y)


class Particle:
    """A round particle affected by gravity and collisions.

    Stores mass, position, velocity and radius. Forces change its
    velocity, and inertial_move then moves it one time step.
    """

    def __init__(self, mass, position, velocity, radius):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.radius = radius

    def inertial_move(self, dt):
        """Move the particle one time step at its current velocity (no forces)."""
        self.position = dt*self.velocity + self.position

    def apply_force(self, dt, f):
        """Apply force vector f for time dt. Changes velocity, not position."""
        a = 1/self.mass*f
        self.velocity = dt*a + self.velocity

    def bounding_box(self):
        """Return the top-left and bottom-right corners of the square around
        the particle. Used by view.py to draw it as a circle."""
        top_left = Vec(self.position.get_coords()[0]-self.radius, self.position.get_coords()[1]+self.radius)
        bottom_right = Vec(self.position.get_coords()[0]+self.radius, self.position.get_coords()[1]-self.radius)

        return top_left, bottom_right


def dot(u, v):
    """Return the dot product of two Vecs."""
    return u.x*v.x + u.y*v.y


def constant_gravitational_field(dt, particles, g=10):
    """Pull every particle straight down, like gravity near the ground.

    Args:
        dt: time step (float)
        particles: list of Particle objects
        g: gravitational acceleration (~10 on Earth)
    """
    for p in particles:
        f = g*p.mass*Vec(0,-1)
        p.apply_force(dt, f)


def circular_arena(dt, particles, k=10000, R=9):
    """Keep particles inside a circle of radius R centred at (0, 0).

    A particle outside the circle is pushed back towards the centre.
    The push grows the further outside it is, like a spring.

    Args:
        dt: time step (float)
        particles: list of Particle objects
        k: wall stiffness (higher = harder wall)
        R: arena radius
    """
    for p in particles:
        r = p.position.norm()
        if R < r:
            f = k * (R - r) * (p.position * (1/r))
            p.apply_force(dt, f)


def wall_force(dt, particles, k, n, a):
    """Make particles bounce off a straight wall.

    The wall is the line through point a with normal n. A particle on
    the wrong side is pushed back, harder the further past the wall it is.

    Args:
        dt: time step (float)
        particles: list of Particle objects
        k: wall stiffness (higher = harder wall)
        n: unit normal Vec of the wall, pointing to the inside
        a: any point on the wall (Vec)
    """
    for p in particles:
        d = dot((p.position-a), n)
        f = -d*k*n
        if d < 0:
            p.apply_force(dt, f)


def gravitational_force(dt, particles, G=15):
    """Apply gravity between every pair of particles.

    Uses Newton's law of gravitation, F = G * m1 * m2 / r^2. Each
    particle sums the pull from all other particles, then the total
    force is applied once.

    Args:
        dt: time step (float)
        particles: list of Particle objects
        G: gravitational constant (strength of gravity)
    """
    for p in particles:
        total = Vec(0, 0)

        for other in particles:
            if other is not p:
                diff = other.position - p.position
                r = diff.norm()
                # Skip overlapping particles: as r -> 0 the force blows up,
                # and collision() handles particles that touch
                if r <= p.radius + other.radius:
                    continue

                F = G * p.mass * other.mass / r**2
                # Turn the magnitude F into a vector pointing at the other particle
                f2 = (F / r) * diff
                total += f2

        p.apply_force(dt, total)


def collision(dt, particles, k=1000000):
    """Make overlapping particles push each other apart.

    Works like a stiff spring: the more two particles overlap, the
    harder they are pushed apart along the line between their centres.

    Args:
        dt: time step (float)
        particles: list of Particle objects
        k: bounce stiffness (higher = harder, less overlap)
    """
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
