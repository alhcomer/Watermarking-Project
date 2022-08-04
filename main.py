from cProfile import label
from doctest import master
from operator import mod
from PIL import Image, ImageTk
from tkinter import BOTH, Button, Tk, Toplevel, filedialog
from tkinter.ttk import Frame, Label


def pop_up_window():
    window = Toplevel()
    window.wm_title("Error")
    label = Label(window, text="Watermark Generator was unable to open that file. Ensure the file type is an image.")
    label.grid(row=0, column=0)
    button = Button(window, text='Okay', command=window.destroy)
    button.grid(row=1, column=0)

class WaterMarkGenerator(Tk):
    # USEFUL RESOURCE https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(MainFrame)

    def switch_frame(self, frame_class):
        # Destroys the current frame and replaces it with a new frame
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destoy()
        self._frame = new_frame
        self._frame.pack()


class MainFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        master.title("Watermark Generator")
        label = Label(self.master, text="Please upload an image to watermark.")
        label.pack(pady=30)
        upload_button = Button(self.master, text='Upload a File', command=self.open_file)
        upload_button.pack(expand=True)
        self.pack(fill=BOTH, expand=1)


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
                self.image = Image.open(fp=self.file_path, mode='r')
                master.switch_frame(CheckImageFrame)
            except IOError:
                pop_up_window()



class CheckImageFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Label(self, text="This is page one").pack()(side="top", fill="x", pady=10)
        




class SaveImageFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        

                
            

            






def main():
    app = WaterMarkGenerator()
    app.geometry('500x200')
    app.mainloop()

if __name__ == '__main__':
    main()



# NEED TO GO THROUGH AND REMOVE UNNECESSARY SELF REFERENCES