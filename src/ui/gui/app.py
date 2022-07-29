import concurrent.futures
import copy
import os
import threading
import time
import tkinter as tk
from queue import Queue
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
    dirs = ObjectProperty(None)  # this is a reference to widget in the main screen
    progress_label = ObjectProperty(None)
    progress_back_button = ObjectProperty(None)
    progress_bar = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)

        self.s = 0
        self.t = 0

        self.total_dirs = 1
        self.current_dir = 1

        self.inp = ''
        self.out = ''
        self.grid_mode = True
        self.stack_mode = False
        self.x_dim = 2
        self.y_dim = 2
        self.framerate = 7
        self.is_gif = False

    def thread_it(self):
        self.dirs = self.dirs.get_dirs()  # this is fetching the info about dirs from the windget in the main screen
        self.total_dirs = len(self.dirs)

        def worker():
            while True:
                item = q.get()
                self.submit(item)
                q.task_done()

                self.current_dir += 1
                self.s = 0

        q = Queue()

        for i in range(1):
            t = threading.Thread(target=worker)
            t.daemon = True
            t.start()

        for item in self.dirs:
            q.put(self.dirs[item])

        # q.join()

        # q = []
        #
        # for d in self.dirs:
        #     q.append(self.dirs[d])
        #
        # with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        #     executor.map(self.submit, q)

        # for d in self.dirs:
        #     self.current_dir = d
        #
        #     self.inp = self.dirs[d]['inp']
        #     self.out = self.dirs[d]['out']
        #     self.grid_mode = self.dirs[d]['grid_mode']
        #     self.stack_mode = self.dirs[d]['stack_mode']
        #     self.x_dim = self.dirs[d]['x_dim']
        #     self.y_dim = self.dirs[d]['y_dim']
        #     self.framerate = self.dirs[d]['framerate']
        #     self.is_gif = self.dirs[d]['is_gif']
        #
        #     t = threading.Thread(target=self.submit, daemon=True, )  # runs the work on a directory in its individual
        #     t.start()

    def update_bar(self, dt):
        self.progress_label.text = "\n".join([f'Directory {self.current_dir} out of {self.total_dirs}...',
                                              f"{self.s} files out of {self.t}..."])

        self.progress_bar.value = self.normalize()

        if self.progress_bar.value == 1 and self.current_dir == self.total_dirs:
            self.progress_label.text += f"\nDONE!"
            self.progress_back_button.opacity = 1
            self.progress_back_button.disabled = False

        elif self.progress_bar.value == 1 and self.current_dir != self.total_dirs:
            self.progress_bar.value = 0

    def normalize(self):
        return (self.s - 0) / (self.t - 0)

    def submit(self, d):
        """
        Function to setup the image processing in the provided folder and mode.

        Takes in input from the GUI to establish the directories and other settings.
        """

        self.inp = d['inp']
        self.out = d['out']
        self.grid_mode = d['grid_mode']
        self.stack_mode = d['stack_mode']
        self.x_dim = d['x_dim']
        self.y_dim = d['y_dim']
        self.framerate = d['framerate']
        self.is_gif = d['is_gif']

        if self.grid_mode:
            self.t = get_total_files(self.inp, files=True)

            for n in fetch_files(path=self.inp,
                                 outpath=self.out,
                                 dim_x=int(self.x_dim),
                                 dim_y=int(self.y_dim)):
                self.s += n
                Clock.schedule_once(self.update_bar)  # updates the progress bar through the Main thread

        elif self.stack_mode:
            self.t = get_total_files(self.inp, dirs=True)

            for n in fetch_dirs(path=self.inp,
                                outpath=self.out,
                                gif=bool(self.is_gif),
                                framerate=int(self.framerate)):
                self.s += n
                Clock.schedule_once(self.update_bar)


class ProgressHeartbeat(Widget):
    pass


class PathButton(Button):
    @staticmethod
    def get_path():
        root = tk.Tk()
        root.withdraw()

        # Alternative of is possible for selection of specific files:
        # return filedialog.askopenfilenames()

        # tkfilebrowser.askopendirnames() from a custom module for tkinker could be modified to select multiple dirs.
        # In particular, if used like in the following code snippet:
        # dirs = tkfilebrowser.askopendirnames(title='File Browser', initialdir=os.path.expanduser("~/Desktop"))
        # return ", ".join(str(x) for x in dirs)

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dirs = {}
        self.total_dirs = 1  # number of dirs
        self.current_dir = 1

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

    def confirm_dir_total(self):
        if self.current_dir >= 10:
            return True

        return False

    def update_counter(self):
        self.ids.current_directory.text = f"Directory {self.current_dir} out of 10..."

    def fill_fields(self):
        if self.current_dir in self.dirs:
            self.inp.text = self.dirs[self.current_dir]['inp']
            self.out.text = self.dirs[self.current_dir]['out']
            self.grid_mode.active = self.dirs[self.current_dir]['grid_mode']
            self.stack_mode.active = self.dirs[self.current_dir]['stack_mode']
            self.x_dim.text = self.dirs[self.current_dir]['x_dim']
            self.y_dim.text = self.dirs[self.current_dir]['y_dim']
            self.framerate.text = self.dirs[self.current_dir]['framerate']
            self.is_gif.active = self.dirs[self.current_dir]['is_gif']

    def clear_fields(self):
        self.inp.text = ""
        self.out.text = ""
        self.grid_mode.active = True
        self.x_dim.text = ""
        self.y_dim.text = ""
        self.framerate.text = ""
        self.is_gif.active = False

    def collect_data(self):

        current = {
            'inp': self.inp.text,
            'out': self.out.text,
            'grid_mode': self.grid_mode.active,
            'stack_mode': self.stack_mode.active,
            'x_dim': self.x_dim.text,
            'y_dim': self.y_dim.text,
            'framerate': self.framerate.text,
            'is_gif': self.is_gif.active
        }

        if not self.check_values():
            self.dirs[self.current_dir] = current

    def back(self):
        self.collect_data()
        self.current_dir -= 1
        self.update_counter()

        if self.current_dir <= 1:
            self.ids.back_button.opacity = 0
            self.ids.back_button.disabled = True

        self.fill_fields()

    def next(self):
        self.collect_data()
        self.current_dir += 1
        self.update_counter()
        self.clear_fields()
        self.ids.back_button.opacity = 1
        self.ids.back_button.disabled = False
        self.fill_fields()

    def change_screen(self):
        self.collect_data()
        self.total_dirs = 1
        self.current_dir = 1
        self.clear_fields()
        self.update_counter()
        self.ids.back_button.opacity = 0
        self.ids.back_button.disabled = True

        App.get_running_app().root.current = "loading_screen"

    def get_dirs(self):
        dirs_copy = copy.deepcopy(self.dirs)
        self.dirs.clear()

        return dirs_copy


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
