from cProfile import label
from doctest import master
from logging import root
from operator import mod
from tkinter.messagebox import YES
from PIL import Image, ImageTk
from tkinter import BOTH, BOTTOM, CENTER, LEFT, Button, PhotoImage, Tk, Toplevel, filedialog, Canvas
from tkinter.ttk import Frame, Label


def pop_up_window():
    window = Toplevel()
    window.wm_title("Error")
    label = Label(window, text="Watermark Generator was unable to open that file. Ensure the file type is an image.")
    label.grid(row=0, column=0)
    button = Button(window, text='Okay', command=window.destroy)
    button.grid(row=1, column=0)

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
                pop_up_window()


class CheckImageFrame(Frame):
    def __init__(self, master, image):
        Frame.__init__(self, master)
        self.image = image
        image_width = self.image.width()
        image_height = self.image.height()
        print(image_width, image_height)
        self.master.geometry(f"{image_width + 20}x{image_height + 70}")
        Label(self, image=image).pack(fill=BOTH, expand=YES)
        # Need to add button commands
        #Use https://stackoverflow.com/questions/2261191/how-can-i-put-2-buttons-next-to-each-other to pack buttons
        Label(self, text="Is this the image you would like to watermark?").pack(side=BOTTOM)
        Button(self, text="Yes", command=None).pack(side=BOTTOM)
        Button(self, text="No", command=None).pack(side=BOTTOM)
        # Need to refit all widgets so that they are in grid instead of pack
        # Geometry setting must happen at the end


class CheckWaterMarkFrame(Frame):
    def __init__(self, master, image):
        Frame.__init__(self, master)
        

class SaveImageFrame(Frame):
    def __init__(self, master, image):
        Frame.__init__(self, master)
        
# NEED TO GO THROUGH AND REMOVE UNNECESSARY SELF REFERENCES

                
            