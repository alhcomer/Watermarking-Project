from cProfile import label
from doctest import master
from logging import root
from operator import mod
from PIL import Image, ImageTk
from tkinter import BOTH, Button, PhotoImage, Tk, Toplevel, filedialog, Canvas
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
        Button(self, text='Upload a File', command=self.open_file).pack(expand=True)

    def open_file(self):
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
        Label(self, text="This is page one").grid(column=1, row=0)
        Label(self, image=image).grid(column=1, row=4)
        

class SaveImageFrame(Frame):
    def __init__(self, master, image):
        Frame.__init__(self, master)
        
# NEED TO GO THROUGH AND REMOVE UNNECESSARY SELF REFERENCES

                
            