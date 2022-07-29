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
```

Where *model* folder contains the logic of the image and animation creation, and the *ui* folder contains files that are responsible 
for instantiation of GUI and CLI variants of the user interface. At the time of writing, *main.py* only enables running code with the GUI.
To use CLI instead, the respective function from *cli* folder needs to be called. This will be changed in the final version of the product.

## Input Format ##

TBU.

## Installation Notes - building from source ##

Copy the GitHub repo in a folder of your choice. 

Create and activate a virtual environment using a tool of your choice.

To build the program, first, make sure you have Python 3.8 or higher installed. If there are any errors to do with the Python version 
in particular, try upgrading to Python 3.10, using *pipenv* or the like Python manager. 

Then, run `pip install requirements.txt`. It should install all the third-party libraries for you.

From their, navigate to *src* folder and run `python main.py` or equivalent. At this step, a GUI should appear on the screen. 

Now, test the program using your own images or download samples from *data* folder.

## Installation Notes - executable ##

TBU.

