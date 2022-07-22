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

import ui.gui.app as app

if __name__ == '__main__':
    app.run()
