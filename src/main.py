"""
This is the main module of the IBERS Image Merger program.
It is responsible for setting up the main module and configuring the behaviour of the program.

The main outputs can be categorized into multiple groups:

    - X x Y grid out of N given photos, where X is number of columns in the grid, and Y is number of rows
    - animations, consisting out of N provided images

"""

__author__ = 'Nika Karsanova'
__email__ = 'vek2@aber.ac.uk'

import ui.gui.app as app
import ui.cli as cli

import argparse

if __name__ == '__main__':
    app.run()
    # cli.arg_init()

    # p = argparse.ArgumentParser()
    # p.add_argument('-gui', type=bool)
    #
    # args = p.parse_args()
    #
    # gui = args.gui or True
    #
    # if gui:
    #     app.run()
    #
    # else:
    #     cli.arg_init()
