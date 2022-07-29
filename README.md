# Roboworm Image Processing — AberForward 2022 Project

This repo contains logic, GUI and CLI configurations of the Roboworm Image Processing project created as part of the AberForward Placement in 2022. 
It was developed for the research team working on Schistosomiasis Research as a matter of automating the process of image analysis produced by Roboworm platform.
Due to that, the functionality is very specific to the needs of the project, though additions can be implemented if needed. At the time fo writing, software is 
configured to quickly produce large amounts of collages and animations in the format specified by the user.

Project was created using Python 3 and Kivy as primary tools, with some third-party libraries such as Pillow, OpenCV and NumPy. 

## Structure ##

The structure of the repo is as follows:

```
├───data
├───src
│   ├───model
│   ├───ui
│   │   └───cli
│   │   └───gui
|   |       └───kv_files
│   ├───main.py
└───README.md
└───requirements.txt
```

Where *model* folder contains the logic of the image and animation creation, and the *ui* folder contains files that are responsible 
for instantiation of GUI and CLI variants of the user interface. At the time of writing, *main.py* only enables running code with the GUI.
To use CLI instead, the respective function from *cli* folder needs to be called. This will be changed in the final version of the product.

## Input Format ##

As was previously mentioned, software is configured to work with a particular structure and specific naming conventions expected 
as the standard output of the Roboworm platform. 

For grid (tiles of images with dimensions in the format of at least 2x2) a folder should be provided, which contains appropriate
image identifier that's what the program uses to determine the images that should be merged together. For samples of that, see `data/grid`
folder.

For stacks (animations), the folder provided should have further folders in it, with the sorted order of these folders denoting the
respectful frames of the animation. For example, in the provided example in the *data* folder, `data/stack/Timepoint_1` denoted frame 1 of 
animations to be created. 

The formats of images currently accepted are limited to the ones accepted by `imread` function of OpenCV: this includes TIFF, PNG, JPEG files 
among some others. 

## Installation Notes ##

### Building from source ###

Copy the GitHub repo in a folder of your choice. 

Create and activate a virtual environment using a tool of your choice.

To build the program, first, make sure you have Python 3.8 or higher installed. If there are any errors to do with the Python version 
in particular, try upgrading to Python 3.10, using *pipenv* or the like Python manager. 

Then, run `pip install requirements.txt`. It should install all the third-party libraries for you.

From their, navigate to *src* folder and run `python main.py` or equivalent. At this step, a GUI should appear on the screen. 

Now, test the program using your own images or download samples from *data* folder.

### Executable ###

TBU.

## Notes ##

Be aware that this piece of software is not yet completed, and has a number of issues that will be addressed during refactoring stage. 
In particular, this concerns data validation topic, performance optimization as well as documentation.

