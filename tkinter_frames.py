from cProfile import label
from doctest import master
from logging import root
from operator import mod
from tkinter.messagebox import YES
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import BOTH, BOTTOM, CENTER, LEFT, Button, PhotoImage, Tk, Toplevel, filedialog, Canvas, Text
from tkinter.ttk import Frame, Label
import matplotlib.pyplot as plt
import pyautogui

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

def error_window():
    window = Toplevel()
    window.wm_title("Error")
    label = Label(window, text="Watermark Generator was unable to open that file. Ensure the file type is an image.")
    label.grid(row=0, column=0)
    button = Button(window, text='Okay', command=window.destroy)
    button.grid(row=1, column=0)
    # TODO: should refactor above label widget making code to single function calls


class WaterMarkGenerator(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(MainFrame)
        self.geometry('900x500')

    def switch_frame(self, frame_class, image=None):
        # Destroys the current frame and replaces it with a new frame
        new_frame = frame_class(self, image)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        

class MainFrame(Frame):
    def __init__(self, master, image):
        Frame.__init__(self, master)
        master.title("Watermark Generator")
        Label(self, text="Please upload an image to watermark.").pack(pady=30)
        Button(self, text='Upload a File', command=self._open_file).pack(expand=True)

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
                self.image = Image.open(self.file_path, mode='r')
                self.tkinter_image = ImageTk.PhotoImage(self.image)
                self.master.switch_frame(CheckImageFrame, image=self.tkinter_image)
            except IOError:
                error_window()

    def _resize_image(self):
        image_width, image_height = self.image.size()
        if image_width > (SCREEN_WIDTH - 50) or image_height > (SCREEN_HEIGHT - 50):
            width_difference = image_width - SCREEN_WIDTH
            height_difference = image_width - SCREEN_HEIGHT
            pass
        # TODO: need to resize image so that both image_width and image_height are 50 less than SCREEN_WIDTH and SCREEN_HEIGHT



class CheckImageFrame(Frame):
    def __init__(self, master, image):
        Frame.__init__(self, master)
        # TODO: scale down image size if greater than screen resolution
        self.image = image
        image_width = self.image.width()
        image_height = self.image.height()
        print(image_width, image_height)
        self.master.geometry(f"{image_width + 20}x{image_height + 70}")
        Label(self, image=image).pack(fill=BOTH, expand=YES)
        # Need to add button commands
        #Use https://stackoverflow.com/questions/2261191/how-can-i-put-2-buttons-next-to-each-other to pack buttons
        Button(self, text="No", command=None).pack(side=BOTTOM)
        Button(self, text="Yes", command=self._choose_watermark).pack(side=BOTTOM)
        Label(self, text="Is this the image you would like to watermark?").pack(side=BOTTOM)

        # Need to refit all widgets so that they are in grid instead of pack
        # Geometry setting must happen at the end

    def _choose_watermark(self):
        window = Toplevel()
        label = Label(window, text="What text would you like to watermark the image with?")
        label.grid(row=0, column=0)
        label2 = Label(window, text="Text must be under 10 characters ")
        label2.grid(row=1, column=0)
        text_box = Text(window, height=1, width=20)
        text_box.grid(row=2, column=0)
        # TODO: need to set text limitations on text box
        # TODO: add font choice drop down box
        Button(window, text="Ok.", command=self._watermark_image).grid(row=3, column=0)
        self.water_mark_text = text_box.get("1.0", "end")
        window.destroy()

    def _watermark_image(self):
        watermark_image = ImageTk.getimage(self.image)
        draw = ImageDraw.Draw(img_to_wm)
        font = ImageFont.truetype("arial.ttf", 50)
        draw.text((0, 0), self.water_mark_text, (0, 0, 0), font=font)
        plt.subplot(1, 2, 1)
        plt.title("black text")
        plt.imshow(watermark_image)
        # img.show()


class CheckWaterMarkFrame(Frame):
    def __init__(self, master, image):
        Frame.__init__(self, master)
        

class SaveImageFrame(Frame):
    def __init__(self, master, image):
        Frame.__init__(self, master)
        
# NEED TO GO THROUGH AND REMOVE UNNECESSARY SELF REFERENCES

                
            