"""
This module sets up the logic of accessing and creating images using ImageGrouper module.
"""

import os

import cv2

import model


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
        s = len(ds) * len(filenames)

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
        ig.grid(size_x=dim_x, size_y=dim_y)
        ig.export_image(filename=filename)

    # time1 = time.time()

    # get files in dir while amending thumbnail variants of images
    files = [x for x in os.listdir(path) if 'Thumb' not in x and 'HTD' not in x]
    files = sorted(files)

    temp = []
    lab: str = ''
    provisional_filename: str = ''
    dir_ref = f"{path.split('/')[-1]}_out"
    os.makedirs(os.path.join(outpath, dir_ref), exist_ok=True)

    for file in files:
        yield 1
        if file[:-4][-1] == '1' and len(temp) != 0:
            process(temp, filename=os.path.join(outpath, dir_ref, provisional_filename), dim_x=dim_x, dim_y=dim_y)
            temp.clear()

        if len(temp) == 0:
            lab = file[-10]  # A, B, C in the name

        if file[-10] != lab:
            continue

        provisional_filename = f"{file[:-4][:-3]}_grid"
        temp.append(cv2.imread(os.path.join(path, file)))

    if len(temp) > 1:
        process(temp, os.path.join(outpath, dir_ref, provisional_filename), dim_x, dim_y)

    # time2 = time.time()
    # print(time2-time1)


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
    # time1 = time.time()

    dirs = [os.path.join(path, x) for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
    dirs = sorted(dirs)

    # fetch names of files to act as first frames
    filenames = [x for x in os.listdir(dirs[0]) if 'Thumb' not in x and 'HTD' not in x]
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

    # time2 = time.time()
    # print(time2 - time1)
