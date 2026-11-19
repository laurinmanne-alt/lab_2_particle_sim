from tkinter import *
from model import *
from time import time

root = Tk()
canvas = Canvas(root, bg="white", width=800, height=600)
canvas.pack()


def to_canvas_coords(canvas, u):
    """Converts simulation coordinates to pixels on the canvas.

    The simulation has (0, 0) in the middle and y going up, the canvas has
    (0, 0) in the top left corner and y going down.
    """
    h = canvas.winfo_reqheight()
    w = canvas.winfo_reqwidth()
    scale = h / 20

    x = scale * u.get_coords()[0]
    y = scale * -u.get_coords()[1]  # minus because y is flipped on the canvas

    return Vec(x + w / 2, y + h / 2)


def move_oval_to(canvas, o, u1, u2):
    """Moves oval o so it fits in the box between corners u1 and u2."""
    x = to_canvas_coords(canvas, u1)
    y = to_canvas_coords(canvas, u2)

    canvas.coords(o, x.x, x.y, y.x, y.y)


def create_oval(canvas, particle):
    """Draws a circle for the particle and returns it."""
    o = canvas.create_oval(80, 30, 140, 150, fill="cyan")
    move_oval_to(canvas, o, particle.bounding_box()[0], particle.bounding_box()[1])
    return o


def simulation_loop(f, timestep, particles):
    """Main loop. f applies the forces, then every particle is moved and redrawn."""
    ovals = []
    for p in particles:
        ovals.append(create_oval(canvas, p))

    time_at_last_frame = 0
    while True:
        f(timestep, particles)

        for p, o in zip(particles, ovals):
            p.inertial_move(timestep)
            move_oval_to(canvas, o, p.bounding_box()[0], p.bounding_box()[1])

        # only update the screen 60 times per second
        if time() - time_at_last_frame >= 1/60:
            canvas.update()
            time_at_last_frame = time()
