"""
This module contains all the main Kivy widgets defined for the purpose of the GUI Functionality.
"""

import copy
import os.path
import threading
import tkinter as tk
from queue import Queue
from tkinter import filedialog

import psutil
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget

from src.model.setup import fetch_files, fetch_dirs, get_total_files, inpath_type

# configuring the minimum window size allowed
Window.minimum_height = 500
Window.minimum_width = 700


class WindowManager(ScreenManager):
    """
    Initialises a Screen manager object, which allows change of screens when necessary.
    """
    pass


class MainScreen(Screen):
    """
    The Main Screen, which holds the functionality of providing, editing and submitting the requirements to run
    data merging on a given directory.
    """
    pass


class LoadingScreen(Screen):
    """
    The Loading Screen, which holds the Progress Bar as well as holds into the backend functions to start the
    data merging process through the config setup in the Main Screen.

    Data is passed through a Widget object initialised in the Main Screen.

    :param msc: the Widget through which the data (e.g., input paths) is accessed
    :param progress_label: reference to the Label object that updates whenever a file is processed
    :param progress_back_button: a Button object, which becomes visible once all the files were processed
    :param progress_bar: the actual progress bar, which is updated every time a file is processed
    """
    msc = ObjectProperty(None)  # this is a reference to widget in the Main Screen
    progress_label = ObjectProperty(None)
    progress_back_button = ObjectProperty(None)
    progress_bar = ObjectProperty(None)

    def __init__(self, **kw):
        """
        Initialises the Screen as well as it's parameters used throughout the program workflow.

        :param kw: a parameter inherited from the Screen Widget

        :param files_processed: how many files from a directory were processed so far
        :param total_files: total number of files in a directory

        :param dirs: dictionary, which contains the configurations to process every directory needed
        :param total_dirs: total number of directories to process
        :param current_dir: number of the directory being processed

        :param inp: input path
        :param out: output path
        :param grid_mode: whether directory is to be processed in grid mode. True - yes.
        :param stack_mode: whether directory is to be processed in stack mode. True - yes.
        :param x_dim: if grid mode is True, number of columns
        :param y_dim: if grid mode is True, number of rows
        :param framerate: if stack mode is True, framerate of animations to produce
        :param is_gif: if True, animations produced will be in GIF format. MP4 otherwise.
        :param parallelism: if True, multi-threads the application
        """
        super().__init__(**kw)

        self.files_processed = 0
        self.total_files = 0

        self.dirs = {}  # data on all directories to be processed from Main Screen widget
        self.total_dirs = 1
        self.current_dir = 1

        self.inp: str = ''
        self.out: str = ''
        self.grid_mode: bool = True
        self.stack_mode: bool = False
        self.x_dim: int = 2
        self.y_dim: int = 2
        self.framerate: int = 7
        self.is_gif: bool = False

        self.parallelism = False

    def thread_it(self):
        """
        Called upon entering the Loading Screen.

        Fetches data from the Main Screen, configures Multithreading and starts worker to process the
        data in the given folder.
        """

        self.parallelism = self.msc.ids.parallelism.active  # if true, run in multithreaded mode

        self.files_processed = 0
        self.total_files = 0

        self.progress_back_button.bind(on_press=self.reset_current_dir_index)

        self.dirs = self.msc.get_dirs()  # this is fetching the info about dirs from the widget in the main screen
        self.total_dirs = len(self.dirs)

        if self.parallelism:  # get total number of files in all provided directories
            for d in self.dirs:
                self.total_files += get_total_files(self.dirs[d]['inp'],
                                                    files=self.dirs[d]['grid_mode'],
                                                    dirs=self.dirs[d]['stack_mode'])

        def worker():
            while True:
                item = q.get()  # directory data -> {'inp': input_path, 'out': output_path ... 'is_gif': False}
                self.submit(item)
                q.task_done()

                if not self.parallelism:
                    self.files_processed = 0

        q = Queue()

        for item in self.dirs:
            q.put(self.dirs[item])

        thread_max = 1 if not self.parallelism else psutil.cpu_count(logical=True) // 2
        thread_max = len(self.dirs) if len(self.dirs) < thread_max else thread_max

        for i in range(thread_max):  # 1 if parallelism ain't selected
            t = threading.Thread(target=worker)
            t.daemon = True
            t.start()

    def update_bar(self, dt):
        """
        Updates the progress bar and it's associated parameters such (i.e., label and button) according to the
        progress of the image merge. Triggered by a Clock event.

        :param dt: delta time, when the even is triggered by the Kivy internal Clock object
        """
        self.progress_label.text = "\n".join([f'Directory {self.current_dir} out of {self.total_dirs}',
                                              f"{self.files_processed} files out of {self.total_files}",
                                              f"{int(self.normalize() * 100)}% out of 100%"])

        self.progress_bar.value = self.normalize()

        def bar_complete():
            self.progress_label.text += f"\nDONE!"
            self.progress_back_button.opacity = 1
            self.progress_back_button.disabled = False

        if not self.parallelism:  # progress bar behaviour if parallelism is NOT enabled
            if self.progress_bar.value == 1 and self.current_dir >= self.total_dirs:
                bar_complete()

            elif self.progress_bar.value == 1 and self.current_dir < self.total_dirs:
                self.progress_bar.value = 0

        if self.parallelism and self.progress_bar.value == 1:
            bar_complete()

    def normalize(self):
        """
        Normalises the value of processed images to total images on the scale of 0 - 1 for easier display in the
        progress bar.
        """
        return (self.files_processed - 0) / (self.total_files - 0)

    def submit(self, d):
        """
        Function to setup the image processing in the provided folder and mode.

        Takes in input from the GUI to establish the directories and other settings.

        Clock object triggers the update of the GUI in the main thread.

        :param d: a dictionary containing information about the entry
        """

        self.inp = d['inp']
        self.out = d['out']
        self.grid_mode = d['grid_mode']
        self.stack_mode = d['stack_mode']
        self.x_dim = d['x_dim']
        self.y_dim = d['y_dim']
        self.framerate = d['framerate']
        self.is_gif = d['is_gif']

        if not self.parallelism:
            self.total_files = get_total_files(d['inp'], files=d['grid_mode'], dirs=d['stack_mode'])

        if self.grid_mode:
            for n in fetch_files(path=self.inp,
                                 outpath=self.out,
                                 dim_x=int(self.x_dim),
                                 dim_y=int(self.y_dim)):
                self.files_processed += n
                Clock.schedule_once(self.update_bar)  # updates the progress bar through the Main thread

        elif self.stack_mode:
            for n in fetch_dirs(path=self.inp,
                                outpath=self.out,
                                gif=bool(self.is_gif),
                                framerate=int(self.framerate)):
                self.files_processed += n
                Clock.schedule_once(self.update_bar)

        self.current_dir += 1

    def reset_current_dir_index(self, instance):
        """
        Upon pressing back button, when all the directories finished processing, resets the current directory counter.

        :param instance: button clicked
        """
        self.current_dir = 1


class ProgressHeartbeat(Widget):
    """
    Widget that holds the progress bar, associated label and button.
    """
    pass


class PathButton(Button):
    """
    Custom button that configures tkinker FileExplorer.
    """

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
    """
    Widget, which collects all the relevant information for data processing in the main screen.

    :param inp: input path
    :param out: output path
    :param grid_mode: whether directory is to be processed in grid mode. True - yes.
    :param stack_mode: whether directory is to be processed in stack mode. True - yes.
    :param x_dim: if grid mode is True, number of columns
    :param y_dim: if grid mode is True, number of rows
    :param framerate: if stack mode is True, framerate of animations to produce
    :param is_gif: if True, animations produced will be in GIF format. MP4 otherwise.
    :param parallelism: if True, multi-threads the application when running the merging.
    """
    inp = ObjectProperty(None)
    out = ObjectProperty(None)
    grid_mode = ObjectProperty(None)
    stack_mode = ObjectProperty(None)
    x_dim = ObjectProperty(defaultvalue=2)
    y_dim = ObjectProperty(defaultvalue=2)
    framerate = ObjectProperty(defaultvalue=7)
    is_gif = ObjectProperty(defaultvalue=False)
    parallelism = ObjectProperty(None)

    def __init__(self, **kwargs):
        """
           Initialises the Widget as well as it's parameters used throughout the program workflow.

           :param kw: a parameter inherited from the Widget class

           :param dirs: stores information on all the directories that need to be analysed
           :param total_dirs: keeps track of total number of directories added, so that specified limit is not exceeded
        """
        super().__init__(**kwargs)

        self.dirs = {}
        self.dirs_limit = 10  # max number of dirs allowed
        self.current_dir = 1

    def check_values(self):
        """
        Function to check whether the required fields were all filled up.

        :return: True if the warning popup should be displayed False otherwise
        """

        grid_reqs = {self.inp.text, self.out.text, self.x_dim.text, self.y_dim.text}
        stack_reqs = {self.inp.text, self.out.text, self.framerate.text}

        dims = {self.x_dim.text, self.y_dim.text}

        grid = self.grid_mode.active and (not all(str.isdigit(d) for d in dims) or "" in grid_reqs)
        stack = self.stack_mode.active and (not str.isdigit(self.framerate.text) or "" in stack_reqs)

        return grid or stack

    def confirm_dir_total(self):
        """
        Functioned used to trigger a warning-popup if a limit of directories is exceeded.

        :return: True if number of directories provided is maxed out, False otherwise.
        """
        return self.current_dir >= self.dirs_limit

    def get_dirs(self):
        """
        Makes a copy of the directory configs provided and returns it, clearing the class attribute.

        :return: a directory, which contains information about the directories to be processed and their settings.
        """
        dirs_copy = copy.deepcopy(self.dirs)
        self.dirs.clear()
        self.parallelism.active = False

        return dirs_copy

    def update_counter(self):
        """
        Updates the label for the UI to track number of directories, which were already made.
        """
        self.ids.current_directory.text = f"Directory {self.current_dir} out of {self.dirs_limit}"

    def fill_fields(self):
        """
        Fills the fields in the main according to the data stored in the dictionary.
        """
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
        """
        Clears the fields in the main screen.
        """
        self.inp.text = ""
        self.out.text = ""
        self.grid_mode.active = True
        self.x_dim.text = ""
        self.y_dim.text = ""
        self.framerate.text = ""
        self.is_gif.active = False

    def collect_data(self):
        """
        Stores the current data provided in a dictionary if all the information needed for a specific
        mode (grid or stack) is provided.
        """

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

        if not self.check_values() and self.path_validation():
            self.dirs[self.current_dir] = current

    def path_validation(self):
        """
        Verifies the existence of the paths to be used for fetching files. Additionally, verifies the structure of files
        is of expected input.

        :return True, if directories are valid. A popup will not be displayed. False otherwise.
        """

        return os.path.isdir(self.inp.text) and os.path.isdir(self.out.text) and inpath_type(
            self.inp.text) == self.grid_mode.active

    def back(self):
        """
        Back button functionality. Binds to the back button in the UI.
        """
        self.collect_data()
        self.current_dir -= 1
        self.update_counter()

        if self.current_dir <= 1:
            self.ids.back_button.opacity = 0
            self.ids.back_button.disabled = True

        self.fill_fields()

    def next(self):
        """
        Next button functionality. Binds to the next button in the UI.
        """
        self.collect_data()
        self.current_dir += 1
        self.update_counter()
        self.clear_fields()
        self.ids.back_button.opacity = 1
        self.ids.back_button.disabled = False
        self.fill_fields()

    def change_screen(self):
        """
        Submit button functionality. Binds to the submit button in the UI to change the screen and reset all the ongoing
        counters.
        """
        self.collect_data()
        # self.total_dirs = 1
        self.current_dir = 1
        self.clear_fields()
        self.update_counter()
        self.ids.back_button.opacity = 0
        self.ids.back_button.disabled = True

        App.get_running_app().root.current = "loading_screen"


class Application(App):
    """
    Used to instantiate application object.
    """
    title = "Roboworm Assistant"
    kv_file = "src/ui/gui/app.kv"
    icon = "resources/icons/worm.png"

    def build(self):
        """
        Builds application object.

        :return: the GUI window
        """
        wm = WindowManager()
        return wm


def run():
    """
    Wrapper for the run function of the Application class, used to initialise a GUI from main module.
    """
    Application().run()
