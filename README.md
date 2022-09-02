# Roboworm Image Processing Assistant — AberForward 2022 Project #

This repo contains logic, GUI and CLI configurations of the Roboworm Image Processing Assistant project created as part of the AberForward Placement in 2022. 
It was developed for the research team working on Schistosomiasis Research as a matter of automating the process of image analysis produced by Roboworm platform.
Due to that, the functionality is very specific to the needs of the project, though additions can be implemented if needed. At the time fo writing, software is 
configured to quickly produce large amounts of collages and animations in the format specified by the user.

Project was created using Python 3 and Kivy as primary tools, with some third-party libraries such as Pillow, OpenCV and NumPy. 

## Structure ##

The structure of the repo is as follows:

```
├───resources
│   │   └───data
│   │   └───icons
├───src
│   ├───model
│   ├───ui
│   │   └───cli
│   │       └───arg.py
│   │   └───gui
│   │       └───app.kv
│   │       └───app.py
│   ├───__main__.py
│
└───cli.py
└───gui.py   
└───README.md
└───requirements.txt
```

Where *model* folder contains the logic of the image and animation creation, and the *ui* folder contains files that are responsible 
for instantiation of GUI and CLI variants of the user interface. The *ui/gui* holds the *.kv* file, acting as a mark-up of the GUI apart from the *.py* file, which 
contains all the functionality. The *cli* folder sets up a parser for the CLI functionality of the program. Finally, the *\_\_main\_\_.py* configures the functions to 
build either the CLI or the GUI, whereas *cli.py* and *gui.py* act as its implementations for the PyInstaller.

In the *resources* folder, under *data* you can find some samples of the images the program is configured to work with and under *icons* folder - copies of the 
icons used for this program.

## Input Format ##

As was previously mentioned, software is configured to work with a particular structure and specific naming conventions expected 
as the standard output of the Roboworm platform. 

For grid (tiles of images with dimensions in the format of at least 2x2) a folder should be provided, which contains appropriate
image identifier (i.e., the name of the image) - that's what the program uses to determine the images that should be merged together. For samples of that, see `data/grid`
folder.

For stacks (animations), the folder provided should have further folders in it, with the sorted order of these folders denoting the
respectful frames of the animation. For example, in the provided example in the *data* folder, `data/stack/Timepoint_1` denotes frame 1 of 
animations to be created. 

The formats of images currently accepted are limited to the ones accepted by `imread` function of OpenCV: this includes TIFF, PNG, and JPEG files. 

## Installation Notes ##

### Running from CMD ###

Copy the GitHub repo in a folder of your choice.

Create and activate a virtual environment using a tool of your choice. Activate it. 

To build the program, navigate to the folder you have copied the repository into. 
Make sure you have Python 3.8 or higher installed. If there are any errors to do with the Python version 
in particular, try upgrading to Python 3.10, using *pipenv* or the like Python manager. 
Then, run `pip install requirements.txt`. It should install all the third-party libraries for you.

From their, run `python gui.py`, `python cli.py` or equivalent. At this step, a GUI or a CLI should appear on the screen. 

Now, test the program using your own images or download samples from *data* folder.

### Building Executable ###

The software, which was used to build an executable of the program is PyInstaller.

To replicate, activate the environment you would result with after performing steps from the [above section](#running-from-cmd).
Run `pip freeze` or `pip install pyinstaller` to make sure that the pyinstaller is installed. 

Now, you can start by running something as simple as `pyinstaller gui.py --onedir -w` command, but, if needed, you can specify
name with `--name` argument, build, dist and spec file directories, name of the program, icon and more. Consult [Pyinstaller Documentation](https://pyinstaller.org/en/stable/)
for more examples.

After that, you will need to modify the generated spec file to attach Kivy hooks as described [here](https://kivy.org/doc/stable/guide/packaging-windows.html).
Once that's done, navigate to the folder that contain the spec file and run `pyinstaller <specfile> -y` to recompile your build.

If you are encountering errors to do with OpenCV binaries, you might need to provide a full path to the *\_\_init\_\_.py*, 
that you can find in your installation of OpenCV. If you are getting errors to do with Kivy imports - double-check that you went 
through [this](https://kivy.org/doc/stable/guide/packaging-windows.html) page in full. If the application opens, but the screen is black
and the UI does not show - there is a problem somewhere to do with you kv file paths.

After your executable is build, a good practice wood be to test it on a website such as [VirusTotal](https://www.virustotal.com/gui/home/upload) 
and then follow [these recommendations](https://python.plainenglish.io/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184)
if it is getting flagged as malicious by various anti-virus products.

If you are happy with your executable, you can use it as is or use a tool like Inno Setup to build an Installer for it.
For example, using a tutorial like [this one](https://www.geeksforgeeks.org/convert-python-code-to-a-software-to-install-on-windows-using-inno-setup-compiler/).

## Application executable ##

You can now download the application using releases on GitHub. Latest release can be found [here](https://github.com/nika-karsanova/aberforward-roboworm/releases/tag/v1.0.1)!

## Notes ##

This piece of software has been thoroughly tested manually, but some bugs may still remain. No additions to the software, however,
are planned at this time.

## References ##

Icon - [Worm icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/worm)
