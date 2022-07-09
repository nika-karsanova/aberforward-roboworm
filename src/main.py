"""
This is the main module of the IBERS Image Merger program.
It is responsible for setting up the main module and configuring the behaviour of the program.

The main outputs can be categorized into multiple groups:

    - (N/2) x 2 grid images out of N given photos, where N is an even number between [2..10]
    - a continuous horizontal merge of N images, where N is number of images between [2..10]
    - animations, consisting out of N provided images, where N is number of images between [2..100]

"""

__author__ = 'Nika Karsanova'
__email__ = 'vek2@aber.ac.uk'

import math
import os

import cv2
from kivy import app
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

import model
from model import constants


class LocalWindowLayout(Widget):
    def __init__(self, **kwargs):
        super(LocalWindowLayout, self).__init__(**kwargs)
        self.files = []
        self.grouper = model.ImageGrouper
        self.path: str = ''

    def selected(self, filename):
        if filename:
            img = Image(source=filename[0], allow_stretch=False)
            self.ids.local_window_carousel.add_widget(img)
            self.files.append(filename[0])

    def fetch_filename(self, index):
        if len(self.files) != 0:
            self.ids.local_window_label.text = self.files[index].split("\\")[-1]

    def action_handler(self, action):
        alt = [cv2.imread(x) for x in self.files]
        self.grouper: model.ImageGrouper = model.ImageGrouper(alt)

        if action == "Merge (grid)":
            self.grouper.grid()

        elif action == "Merge (strip)":
            self.grouper.strip()

        elif action == "Merge (animation)":
            self.grouper.animation(gif=True)

        btn = Button(text='View Results')
        btn.bind(on_press=self.get_output_img)
        self.ids.local_navbar.add_widget(btn)

    def get_output_img(self, instance):
        self.grouper.data.seek(0)
        self.grouper.export_image()
        in_mem = CoreImage(self.grouper.data, ext='png')
        app = App.get_running_app()
        app.root.ids.results_window.ids.output_img.texture = in_mem.texture
        app.root.current = "results"

    def get_default_path(self):
        self.path = os.path.expanduser("~/Desktop")
        return self.path  # sets the root path


class SetupWindow(Screen):
    pass


class LocalFileManagerWindow(Screen):
    def __init__(self, **kw):
        super(LocalFileManagerWindow, self).__init__(**kw)
        lwl = LocalWindowLayout()
        self.add_widget(lwl)


class RemoteFileManagerWindow(Screen):
    pass


class ResultsWindow(Screen):
    def __init__(self, **kw):
        super(ResultsWindow, self).__init__(**kw)


class WindowManager(ScreenManager):
    pass


class Application(App):
    def build(self):
        Builder.load_file("ui/kv_files/main.kv")
        self.title = "IBERS Image Grouper"
        wm = WindowManager()
        return wm


def process(temp, filename: str = "test.png"):
    dim = int(math.sqrt(len(temp)))  # accounting only for square grid

    ig = model.ImageGrouper(temp[:dim * dim])
    print("dim", dim, "len", len(temp))
    print(filename)
    ig.grid(size_x=dim, size_y=dim)
    ig.export_image(filename=filename)


def main():
    files = {x: cv2.imread(os.path.join(constants.PATH1, x)) for x in os.listdir(constants.PATH1)}  # get files in dir

    temp = []
    lab: str = ''
    provisional_filename: str = ''

    for file in files:
        if 'Thumb' in file:  # ammend thumbnail variants of images
            continue

        if file[:-4][-1] == '1' and len(temp) != 0:
            process(temp, filename=provisional_filename)
            temp.clear()

        if len(temp) == 0:
            lab = file[-10]  # A, B, C in the name

        if file[-10] != lab:
            continue

        temp.append(files[file])
        provisional_filename = f"{file[:-4][:-3]}_merged.png"

    if len(temp) > 1:
        process(temp, provisional_filename)


if __name__ == '__main__':
    Application().run()