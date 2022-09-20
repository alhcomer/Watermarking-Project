from cProfile import label
from doctest import master
from email.mime import image
from logging import root
from operator import mod
import re
from sqlite3 import Row
from tkinter import (BOTH, BOTTOM, CENTER, END, LEFT, RIGHT, Button, Canvas, OptionMenu,
                     PhotoImage, StringVar, Text, Tk, Toplevel, filedialog)
from tkinter.messagebox import YES
from tkinter.ttk import Frame, Label
import matplotlib.pyplot as plt
import pyautogui
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageTk

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

def error_window():
    window = Toplevel()
    window.wm_title("Error")
    Label(window, text="Watermark Generator was unable to open that file. Ensure the file type is an image.").grid(row=0, column=0)
    button = Button(window, text='Okay', command=window.destroy)
    button.grid(row=1, column=0)

class WaterMarkGenerator(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.iconbitmap("icons\wm.ico")
        self._frame = None
        self.switch_frame(MainFrame)
        self.geometry('900x500')

    def switch_frame(self, frame_class, image=None, text=None):
        # Destroys the current frame and replaces it with a new frame
        new_frame = frame_class(self, image, text)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid(column=0, row=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        

class MainFrame(Frame):
    def __init__(self, master, image, text):
        Frame.__init__(self, master)
        master.title("Watermark Generator")
        Label(self, text="Please upload an image to watermark.").grid(row=0, column=1)
        Button(self, text='Upload a File', command=self._open_file).grid(row=1, column=1)

    def _open_file(self):
        self.file_path = filedialog.askopenfilename(
            initialdir='/',
            filetypes = (
                ('JPEG', '*.jpg'),
                ('PNF', '*.png'),
                ('All files', '*.*') 
            )
        )
        if self.file_path is not None:
            try:
                self.image = Image.open(self.file_path)
                self.resized_image = self.resize_image(self.image)
                self.tkinter_image = ImageTk.PhotoImage(self.resized_image)
                self.master.switch_frame(CheckImageFrame, image=self.tkinter_image)
            except IOError:
                error_window()

    def resize_image(self, image):
        image_width, image_height = image.size
        print(image_width, image_height)
        if image_width > (SCREEN_WIDTH - 100) or image_height > (SCREEN_HEIGHT - 100):
            image = image.resize((image_width - 500, image_height - 500))
            # TODO: improve efficiency of resizing method
            image = self.resize_image(image)
        return image


class CheckImageFrame(Frame):
    def __init__(self, master, image, text):
        Frame.__init__(self, master)
        self.image = image
        image_width = self.image.width()
        image_height = self.image.height()
        self.toplevel = None
        self.master.geometry(f"{image_width + 100}x{image_height + 150}")
        Label(self, image=image).grid(column=0, row=0)
        Label(self, text="Is this the image you would like to watermark?").grid(column=0, row=1)
        self.button_frame = Frame(master=self)
        Button(self.button_frame, text="Yes", command=self._choose_watermark).grid(column=0, row=0, padx=10)
        Button(self.button_frame, text="No", command=self._to_first_frame).grid(column=1, row=0, padx=10)
        self.button_frame.grid(column=0, row=2, pady=10)

    def _choose_watermark(self):
        # TODO: add font choice drop down box - low priority
        # TODO: add colour options to the watermark generator

        font_options = [
            
        ]

        if self.toplevel == None:
            self.toplevel = Toplevel()
            label = Label(self.toplevel, text="What text would you like to watermark the image with?")
            label.grid(row=0, column=0, padx=10)
            label2 = Label(self.toplevel, text="Text must be under 10 characters ")
            label2.grid(row=1, column=0, padx=10)
            self.text_box = Text(self.toplevel, height=1, width=20)
            self.text_box.grid(row=2, column=0, padx=10)
            self.btn = Button(self.toplevel, text="Ok.", command=self._to_check_wm)
            self.btn.grid(row=3, column=0, padx=10)
            self.toplevel.bind('<Return>', lambda event: self._to_check_wm())

    def _to_first_frame(self):
        self.master.switch_frame(MainFrame)
        
    def _to_check_wm(self):
        self.water_mark_text = self.text_box.get(1.0, END)
        if len(self.water_mark_text) < 11 and self.water_mark_text and self.water_mark_text.strip():
            self.toplevel.destroy()
            self.master.switch_frame(CheckWaterMarkFrame, image=self.image, text=self.water_mark_text)
            

class CheckWaterMarkFrame(Frame):
    def __init__(self, master, image, text):
        Frame.__init__(self, master)
        self.text = text
        self.image = image
        self.tk_watermark_image = self.watermark_image()
        Label(self, image=self.tk_watermark_image).grid(column=0, row=0)
        Label(self, text="Is this image watermarked how you would like?").grid(column=0, row=1)
        self.button_frame = Frame(master=self)
        Button(self.button_frame, text="Yes", command=self._download_image).grid(column=0, row=0, padx=10)
        Button(self.button_frame, text="No", command=self._back_to_check_image).grid(column=1, row=0, padx=10)
        self.button_frame.grid(column=0, row=2)
        

    def watermark_image(self):
        self.watermark_image = ImageTk.getimage(self.image).copy()
        font = ImageFont.truetype("arial.ttf", 50)
        wm_text = Image.new('L', (100, 100))
        draw = ImageDraw.Draw(wm_text)
        draw.text((0, 0), self.text, font=font, fill=255)
        w = wm_text.rotate(45, expand=1)


        image_width, image_height = self.watermark_image.size
        for x in range(0, image_width, 150):
            for y in range(0, image_height, 150):
                self.watermark_image.paste(ImageOps.colorize(w, (0,0,0), (255,255,84)), (x, y),  w)

        plt.imshow(self.watermark_image)
        plt.show()
        self.tk_watermark_image = ImageTk.PhotoImage(self.watermark_image)
        return self.tk_watermark_image

    def _back_to_check_image(self):
        self.master.switch_frame(CheckImageFrame, image=self.image)

    def _download_image(self):
        file = filedialog.asksaveasfile(mode='w', 
        defaultextension='.jpg', filetypes=(
                ('JPEG', '*.jpg'),
                ('PNF', '*.png'),
                ('All files', '*.*') 
            ))
        if not file:
            return 
        self.rgb_image = self.watermark_image.convert('RGB')
        self.rgb_image.save(file)


# TODO: go through and delete unnecessary self references
# TODO: go through button commands and make them lambda expressions
# example of doing so in answer here:
# https://stackoverflow.com/questions/14824163/how-to-get-the-input-from-the-tkinter-text-widget
