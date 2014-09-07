# -*- coding: utf-8 -*-
__author__ = 'jgo'
from tkinter import *


fen = Tk()
fen.title("PyLaby v0.1")

can = Canvas(fen, width=500, height=500)

photo_wall = PhotoImage(file="sprite/wall.png")
sprite_wall = can.create_image(0, 0, anchor=NW, image=photo_wall)

can.pack()

fen.mainloop()