# Task (7/12): Draw on canvas
from tkinter import *
from model import *
canvas = Canvas(Tk(), bg="white", width=800, height=600)
canvas.pack()
o = canvas.create_oval(80, 30, 140, 150, fill="blue")
input()

# Task (8/12): Define a new function to_canvas_coords(canvas, x)
def to_canvas_coords(canvas, u):
    h = canvas.winfo_reqheight()
    w = canvas.winfo_reqwidth()
    scale = h / 20

    x = scale * u[0]
    y = scale * -u[1]

    return (x + w / 2, y + h / 2)

#######################################
### NB. Task 9 is done in model.py. ###
#######################################

# Task (10/12): Define a new function move_oval_to(canvas, o, u1, u2)

# Task (11/12): Define a new function create_oval(canvas, particle)
def create_oval(canvas, particle):
    o = canvas.create_oval(80, 30, 140, 150, fill="blue")
    pos = particle.position
    r = particle.radius
    move_oval_to(canvas, o, pos - r, pos + r)
    return o

# Task (12/12): Define a function simulation_loop(f, timestep, particles)
def simulation_loop(f, timestep, particles):
    ovals = []
    for p in particles:
        ovals.append(create_oval(canvas, p))

    while True:
        f(timestep, particles)
        
        for p, o in zip(particles, ovals):
            i.inertial_move(timestep)
            move_oval_to(canvas, o, i.bounding_box[0], i.bounding_box[1])

        canvas.update()