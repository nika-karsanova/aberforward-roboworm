"""
This is the main module of the IBERS Image Merger program.
It is responsible for setting up the main module and configuring the behaviour of the GUI.

The main outputs can be categorized into multiple groups:

    - X x Y grid out of N given photos, where X is number of columns in the grid, and Y is number of rows
    - animations, consisting out of N provided images

"""

__author__ = 'Nika Karsanova'
__email__ = 'vek2@aber.ac.uk'

import os
import sys

from kivy.resources import resource_add_path, resource_find

import src.ui.cli.arg as arg
from src.ui.gui import app


def gui_main():
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    app.run()


def cli_main():
    arg.arg_init()


if __name__ == '__main__':
    gui_main()
