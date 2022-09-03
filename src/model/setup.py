"""
This module sets up the logic of accessing and creating images using ImageGrouper module.
"""

import os
import re

import cv2

import src.model.image_grouper as model


def inpath_type(inpath: str):
    """
    Return True if path provided is suitable for creation of grid images.
    False if path provided is suitable for creation of stack images.
    None, if path does not have valid contents.

    :param inpath: path to check
    """
    frame_dirs = []

    for root, dirs, files in os.walk(inpath):
        # grid
        if root == inpath and len(dirs) == 0 and all(x.lower().endswith(('tif', 'png', 'jpg', 'htd')) for x in files):
            return True

        # stack root
        elif root == inpath and len(files) == 1 and all(x.lower().endswith('htd') for x in files) and all(
                re.search(r'\d+$', x) for x in dirs):  # if dir name is of correct format
            frame_dirs = dirs
            continue

        # stack folders
        elif os.path.split(root)[-1] in frame_dirs and len(dirs) == 0 and all(
                x.lower().endswith(('tif', 'png', 'jpg', 'htd')) for x in files):
            continue

        else:
            return None

    return False


def get_total_files(path: str,
                    files: bool = None,
                    dirs: bool = None):
    """
    Calculates total number of files to display in the progress bar.

    :param path: input path
    :param files: True if path contains image files in it
    :param dirs: True if path contains further directories in it
    :return: number of files in the input path
    """
    s = 0

    if files:
        s = len([x for x in os.listdir(path) if 'Thumb' not in x and 'HTD' not in x])

    elif dirs:
        ds = [os.path.join(path, x) for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
        filenames = [x for x in os.listdir(ds[0]) if 'Thumb' not in x and 'HTD' not in x]
        # not accurate number of files, but alligns with the count produced as a result of fetch_dirs() generator
        s = len(ds) * len(filenames)

        # accurate number of files if needed
        # for d in ds:
        #     s += len([x for x in os.listdir(d) if 'Thumb' not in x and 'HTD' not in x])

    return s


def fetch_files(path: str,
                outpath: str,
                dim_x: int,
                dim_y: int):
    """
    Identifies images that should be merged together via the naming convention.

    :param path: input path
    :param outpath: output path
    :param dim_x: columns
    :param dim_y: rows
    :return: yields 1 whenever a file is processed
    """

    def process(temp: list,
                filename: str = "test",
                dim_x: int = 2,
                dim_y: int = 2):

        """
        Create an ImageGrouper object and pass the files to be merged together.

        :param temp: the images to merge together
        :param filename: filename
        :param dim_x: columns
        :param dim_y: rows
        :return:
        """

        ig = model.ImageGrouper(temp[:dim_x * dim_y])

        export = ig.grid(size_x=dim_x, size_y=dim_y)
        if export:
            ig.export_image(filename=filename)

    # get files in dir while amending thumbnail variants of images
    files = [x for x in os.listdir(path) if 'thumb' not in x.lower() and 'htd' not in x.lower()]
    files = sorted(files)

    temp = []
    lab: str = ''
    provisional_filename: str = ''
    dir_ref = f"{path.split('/')[-1]}_out"
    os.makedirs(os.path.join(outpath, dir_ref), exist_ok=True)

    for file in files:
        yield 1

        try:
            if file[:-4][-1] == '1' and len(temp) != 0:
                process(temp, filename=os.path.join(outpath, dir_ref, provisional_filename), dim_x=dim_x, dim_y=dim_y)
                temp.clear()

            if len(temp) == 0 and file[:-4][-1] == '1':
                lab = file[-10]  # A, B, C in the name

            if file[-10] != lab:
                continue

            provisional_filename = f"{file[:-4][:-3]}_grid"
            temp.append(cv2.imread(os.path.join(path, file)))

        except IndexError:
            continue

    if len(temp) > 1:
        process(temp, os.path.join(outpath, dir_ref, provisional_filename), dim_x, dim_y)


def fetch_dirs(path: str,
               outpath: str,
               gif: bool = False,
               framerate: int = 1):
    """
    Initialises creation of the animations through fetching the frames one by one for all files in
    the input path/frame1 folders (e.g., Samples/Timepoint_1).

    :param path: input path
    :param outpath: output path
    :param gif: if True, animation returned is in GIF format, MP4 otherwise
    :param framerate: sets up framerate, 1 by default

    :return yields 1 whenever a new file is being processed
    """

    dirs = [os.path.join(path, x) for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
    dirs = sorted(dirs)

    # fetch names of files to act as first frames
    filenames = [x for x in os.listdir(dirs[0]) if 'thumb' not in x.lower() and 'htd' not in x.lower()]
    dir_ref = f"{path.split('/')[-1]}_out"
    os.makedirs(os.path.join(outpath, dir_ref), exist_ok=True)

    temp = []

    for f in filenames:
        for d in dirs:
            yield 1

            if f in os.listdir(d):
                temp.append(cv2.imread(os.path.join(d, f)))  # numpy array of frames

        ig = model.ImageGrouper(temp)
        ig.animation(framerate=framerate, gif=gif, filename=os.path.join(outpath, dir_ref, f"{f[:-4]}_stack"))
        temp.clear()
