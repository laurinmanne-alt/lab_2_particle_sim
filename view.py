# Task (7/12): Draw on canvas
from tkinter import *
from model import *
from time import time

root = Tk()
canvas = Canvas(root, bg="white", width=800, height=600)
canvas.pack()   

# Task (8/12): Define a new function to_canvas_coords(canvas, x)
# Function: Omvandlar positioner till ett talsystem på canvasen
# Input: Ett canvas objekt och en x/y koordinat som en tupel
# Output: Returnerar tillbaka värderna fast omformatterade för koordinatsystem
def to_canvas_coords(canvas, u):
    print(type(u))
    h = canvas.winfo_reqheight()
    w = canvas.winfo_reqwidth()
    scale = h / 20

    x = scale * u[0]
    y = scale * -u[1]

    return (x + w / 2, y + h / 2)

#######################################
### NB. Task 9 is done in model.py. ###
#######################################

# Function: Flyttar en oval till specifika koordinater
# Input: Ett canvas objekt, oval objektet som ska flyttas, u1 och u2 skapar omkretsen för kvadratområdet där cirkeln hmanr
# Output: null
# Task (10/12): Define a new function move_oval_to(canvas, o, u1, u2)
def move_oval_to(canvas, o, u1, u2):
    x = to_canvas_coords(canvas, u1)
    y = to_canvas_coords(canvas, u2)

    canvas.coords(o, x[0], x[1], y[0], y[1])

# Task (11/12): Define a new function create_oval(canvas, particle)
# Function: Skapar en oval och flyttar den till den tilldelade particlen
# Input: Ett canvas objekt och ett partikel objekt
# Output: Returnerar cirkel objektet
def create_oval(canvas, particle):
    o = canvas.create_oval(80, 30, 140, 150, fill="cyan")
    move_oval_to(canvas, o, particle.bounding_box()[0], particle.bounding_box()[1])
    return o

# Task (12/12): Define a function simulation_loop(f, timestep, particles)
def simulation_loop(f, timestep, particles):
    ovals = []
    for p in particles:
        ovals.append(create_oval(canvas, p))

    time_at_last_frame = 0
    while True:
        f(timestep, particles)
        
        for p, o in zip(particles, ovals):
            p.inertial_move(timestep)
            move_oval_to(canvas, o, p.bounding_box()[0], p.bounding_box()[1])

        if time() - time_at_last_frame >= 1/30:
            canvas.update()
            time_at_last_frame = time()