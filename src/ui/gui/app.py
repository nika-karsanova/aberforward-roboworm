import tkinter as tk
from tkinter import filedialog

from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.widget import Widget

from model.setup import fetch_files, fetch_dirs

# configuring the minimum window size allowed
Window.minimum_height = 500
Window.minimum_width = 700


class PathButton(Button):
    @staticmethod
    def get_path():
        root = tk.Tk()
        root.withdraw()

        # alternative of return filedialog.askopenfilenames() is possible for selection of specific files
        return filedialog.askdirectory()


class WindowsFileChooser(Widget):
    inp = ObjectProperty(None)
    out = ObjectProperty(None)
    grid_mode = ObjectProperty(None)
    stack_mode = ObjectProperty(None)
    x_dim = ObjectProperty(defaultvalue=2)
    y_dim = ObjectProperty(defaultvalue=2)
    framerate = ObjectProperty(defaultvalue=7)
    is_gif = ObjectProperty(defaultvalue=False)

    def check_values(self):
        """
        Function to check whether the required fields were all filled up.

        :return: True if the warning popup should be displayed False otherwise
        """

        grid_reqs = {self.inp.text, self.out.text, self.x_dim.text, self.y_dim.text}
        stack_reqs = {self.inp.text, self.out.text, self.framerate.text}

        if self.grid_mode.active and "" in grid_reqs or self.stack_mode.active and "" in stack_reqs:
            return True

        return False

    def submit(self):
        """
        Function to setup the image processing in the provided folder and mode.

        Takes in input from the GUI to establish the directories and other settings.
        """

        inp = self.inp.text
        out = self.out.text
        x_dim = self.x_dim.text
        y_dim = self.y_dim.text
        framerate = self.framerate.text
        is_gif = self.is_gif.active

        if self.grid_mode.active:
            fetch_files(path=inp, outpath=out, dim_x=int(x_dim), dim_y=int(y_dim))

        elif self.stack_mode.active:
            fetch_dirs(path=inp, outpath=out, gif=bool(is_gif), framerate=int(framerate))


class Application(App):
    """
    Used to instantiate application object.
    """
    title = "Roboworm Image Grouper"
    kv_file = "ui/gui/kv_files/app.kv"

    def build(self):
        """
        Builds application object.

        :return: the GUI window
        """
        return WindowsFileChooser()


def run():
    Application().run()
