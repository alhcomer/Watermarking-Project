from tkinter_frames import WaterMarkGenerator
from tkinter_frames import SCREEN_WIDTH, SCREEN_HEIGHT


def center(window):
    window.update_idletasks()
    size = tuple(int(_) for _ in window.geometry().split("+")[0].split("x"))
    x = SCREEN_WIDTH / 2 - size[0] / 2
    y = SCREEN_HEIGHT / 2 - size[1] / 2
    window.geometry("+%d+%d" % (x, y))


def main():
    app = WaterMarkGenerator()
    center(app)

    app.mainloop()


if __name__ == "__main__":
    main()
