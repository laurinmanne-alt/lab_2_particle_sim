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
    h = canvas.winfo_reqheight()
    w = canvas.winfo_reqwidth()
    scale = h / 20

    x = scale * u.get_coords()[0]
    y = scale * -u.get_coords()[1]

    return Vec(x + w / 2, y + h / 2)


# Function: Flyttar en oval till specifika koordinater
# Input: Ett canvas objekt, oval objektet som ska flyttas, u1 och u2 skapar omkretsen för kvadratområdet där cirkeln hmanr
# Output: null
# Task (10/12): Define a new function move_oval_to(canvas, o, u1, u2)
def move_oval_to(canvas, o, u1, u2):
    x = to_canvas_coords(canvas, u1)
    y = to_canvas_coords(canvas, u2)

    canvas.coords(o, x.x, x.y, y.x, y.y)


# Task (11/12): Define a new function create_oval(canvas, particle)
# Function: Skapar en oval och flyttar den till den tilldelade particlen
# Input: Ett canvas objekt och ett partikel objekt
# Output: Returnerar cirkel objektet
def create_oval(canvas, particle):
    o = canvas.create_oval(80, 30, 140, 150, fill="cyan")
    move_oval_to(canvas, o, particle.bounding_box()[0], particle.bounding_box()[1])
    return o


# Function: Ritar en rund circel i mitten av fönstret med samma radie som den runda arenan.
# Input: canvas är objektet med rutan/fönstret, to_canvas_coords är en function som omvandlar vanliga koordonater till canvas koordinater, R är radien på cirkeln.
# Output: null
def create_graphic_wall(R):
    x0, y0 = to_canvas_coords(canvas, Vec(-R, R)).get_coords()
    x1, y1 = to_canvas_coords(canvas, Vec(R, -R)).get_coords()
    
    canvas.create_oval(x0, y0, x1, y1, outline="black")


# Task (12/12): Define a function simulation_loop(f, timestep, particles)
# Function: Programmets huvudloop som går medan simulationen är igång. Loopen kallar på funktioner som skapar de grafiska objekten för partiklarna och kallar på kraft funktionerna som påverkar partiklarnas beteende. 
# Output: null
def simulation_loop(f, timestep, particles):
    ovals = []
    for p in particles:
        ovals.append(create_oval(canvas, p))

    create_graphic_wall(9)  # Kommentera ut för att ta bort den runda cirkeln i UI och ändra parametern så den matchat med circular_arena radien. Kom verkligen inte på någon bättre lösning :*(

    time_at_last_frame = 0
    while True:
        f(timestep, particles)
        
        for p, o in zip(particles, ovals):
            p.inertial_move(timestep)
            move_oval_to(canvas, o, p.bounding_box()[0], p.bounding_box()[1])

        if time() - time_at_last_frame >= 1/30:
            canvas.update()
            time_at_last_frame = time()