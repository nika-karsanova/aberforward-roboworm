import os
import threading
import time
import tkinter as tk
from tkinter import filedialog
import tkfilebrowser

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget

from model.setup import fetch_files, fetch_dirs, get_total_files

# configuring the minimum window size allowed
Window.minimum_height = 500
Window.minimum_width = 700


class WindowManager(ScreenManager):
    pass


class MainScreen(Screen):
    pass


class LoadingScreen(Screen):
    inp = ObjectProperty(None)
    out = ObjectProperty(None)
    grid_mode = ObjectProperty(None)
    stack_mode = ObjectProperty(None)
    x_dim = ObjectProperty(defaultvalue=2)
    y_dim = ObjectProperty(defaultvalue=2)
    framerate = ObjectProperty(defaultvalue=7)
    is_gif = ObjectProperty(defaultvalue=False)

    def __init__(self, **kw):
        super().__init__(**kw)

        self.s = 0
        self.t = 0

    def thread_it(self):
        threading.Thread(target=self.submit).start()

    def update_bar(self, dt):
        self.ids.progress_widget.ids.progress_bar_label.text = f'{self.s} out of {self.t}...'

        if self.ids.progress_widget.ids.progress_bar.value == 1:
            self.s = 0
            self.ids.progress_widget.ids.progress_bar_button.opacity = 1

        self.ids.progress_widget.ids.progress_bar.value = self.normalize()

    def normalize(self):
        return (self.s - 0) / (self.t - 0)

    def submit(self):
        """
        Function to setup the image processing in the provided folder and mode.

        Takes in input from the GUI to establish the directories and other settings.
        """

        if self.grid_mode.active:
            self.t = get_total_files(self.inp.text, files=True)

            for n in fetch_files(path=self.inp.text,
                                 outpath=self.out.text,
                                 dim_x=int(self.x_dim.text),
                                 dim_y=int(self.y_dim.text)):
                self.s += n
                Clock.schedule_once(self.update_bar)

        elif self.stack_mode.active:
            self.t = get_total_files(self.inp.text, dir=True)

            fetch_dirs(path=self.inp.text,
                       outpath=self.out.text,
                       gif=bool(self.is_gif.active),
                       framerate=int(self.framerate.text))


class ProgressHeartbeat(Widget):
    pass


class PathButton(Button):
    @staticmethod
    def get_path():
        root = tk.Tk()
        root.withdraw()

        # alternative of return filedialog.askopenfilenames() is possible for selection of specific files
        # tkfilebrowser.askopendirnames() from a custom module for tkinker could be modified to select multiple dirs
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

    @staticmethod
    def check_screen():
        App.get_running_app().root.current = "loading_screen"


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
        wm = WindowManager()
        return wm


def run():
    Application().run()
