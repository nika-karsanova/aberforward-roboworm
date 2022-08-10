"""
This is the main module of the IBERS Image Merger program.
It is responsible for setting up the main module and configuring the behaviour of the GUI.

This file is an entry point of the Command-Line Interface.

The main outputs can be categorized into multiple groups:

    - X x Y grid out of N given photos, where X is number of columns in the grid, and Y is number of rows
    - animations, consisting out of N provided images

"""

__author__ = 'Nika Karsanova'
__email__ = 'vek2@aber.ac.uk'

import ui.cli.arg as arg

if __name__ == '__main__':
    arg.arg_init()