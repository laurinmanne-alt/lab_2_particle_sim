"""Drawing and main loop for the particle simulation (Tkinter)."""

from tkinter import *
from model import *
from time import time

root = Tk()
canvas = Canvas(root, bg="white", width=800, height=600)
canvas.pack()


def to_canvas_coords(canvas, u):
    """Convert a simulation position to canvas pixel coordinates.

    The simulation has (0, 0) in the middle and y pointing up. The canvas
    has (0, 0) in the top-left corner and y pointing down, so y is flipped
    and everything is shifted to the centre. The visible area is 20
    simulation units tall.

    Args:
        canvas: the Tkinter Canvas to draw on
        u: position in simulation coordinates (Vec)

    Returns:
        the same position in canvas pixels (Vec)
    """
    h = canvas.winfo_reqheight()
    w = canvas.winfo_reqwidth()
    scale = h / 20

    x = scale * u.get_coords()[0]
    # Minus sign flips y: up in the simulation is down on the canvas
    y = scale * -u.get_coords()[1]

    return Vec(x + w / 2, y + h / 2)


def move_oval_to(canvas, o, u1, u2):
    """Move an oval so it fills the box between two corners.

    Args:
        canvas: the Tkinter Canvas
        o: id of the oval to move
        u1: top-left corner in simulation coordinates (Vec)
        u2: bottom-right corner in simulation coordinates (Vec)
    """
    x = to_canvas_coords(canvas, u1)
    y = to_canvas_coords(canvas, u2)

    canvas.coords(o, x.x, x.y, y.x, y.y)


def create_oval(canvas, particle):
    """Draw a circle for a particle and place it at the particle's position.

    Returns:
        the id of the new oval, used later to move it
    """
    # Start coordinates don't matter, move_oval_to places it right away
    o = canvas.create_oval(80, 30, 140, 150, fill="cyan")
    move_oval_to(canvas, o, particle.bounding_box()[0], particle.bounding_box()[1])
    return o


def calls_function(func, target_name):
    """Return True if func calls a function named target_name."""
    return target_name in func.__code__.co_names


def simulation_loop(f, timestep, particles):
    """Run the simulation forever and draw it.

    Each step applies the forces, moves every particle and its circle,
    and redraws the window at most 60 times per second.

    Args:
        f: function f(dt, particles) that applies all forces
        timestep: simulated time per step (float)
        particles: list of Particle objects
    """
    ovals = []
    for p in particles:
        ovals.append(create_oval(canvas, p))

    time_at_last_frame = 0
    while True:
        f(timestep, particles)

        for p, o in zip(particles, ovals):
            p.inertial_move(timestep)
            move_oval_to(canvas, o, p.bounding_box()[0], p.bounding_box()[1])

        # Physics runs every loop, but the screen only redraws at 60 FPS
        if time() - time_at_last_frame >= 1/60:
            canvas.update()
            time_at_last_frame = time()
