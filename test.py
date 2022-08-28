from cProfile import label
from doctest import master
from email.mime import image
from logging import root
from operator import mod
from sqlite3 import Row
from tkinter.messagebox import YES
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps
from tkinter import BOTH, BOTTOM, CENTER, END, LEFT, RIGHT, Button, PhotoImage, Tk, Toplevel, filedialog, Canvas, Text
from tkinter.ttk import Frame, Label
import matplotlib.pyplot as plt
import pyautogui
im=Image.open("X:\Aidan Comer\Pictures\Saved Pictures\hummingbird.jpg")

f = ImageFont.load_default()
txt=Image.new('L', (500,50))
d = ImageDraw.Draw(txt)
d.text( (0, 0), "Someplace Near Boulder",  font=f, fill=255)
w=txt.rotate(17.5,  expand=1)

im.paste( ImageOps.colorize(w, (0,0,0), (255,255,84)), (242,60),  w)

im.show()