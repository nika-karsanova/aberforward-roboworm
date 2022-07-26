import os

import cv2

import model
import time


def process(temp,
            filename: str = "test",
            dim_x: int = 2,
            dim_y: int = 2):
    ig = model.ImageGrouper(temp[:dim_x * dim_y])
    ig.grid(size_x=dim_x, size_y=dim_y)
    ig.export_image(filename=filename)


def get_total_files(path: str,
                    files: bool = None,
                    dir: bool = None):
    s = 0

    if files:
        s = len([x for x in os.listdir(path) if 'Thumb' not in x])

    elif dir:
        dirs = [os.path.join(path, x) for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]

        for d in dirs:
            s += len([x for x in os.listdir(d) if 'Thumb' not in x])

    return s


def fetch_files(path: str,
                outpath: str,
                dim_x: int,
                dim_y: int):
    # time1 = time.time()
    # get files in dir while amending thumbnail variants of images
    # files = {x: cv2.imread(os.path.join(path, x)) for x in os.listdir(path) if 'Thumb' not in x}

    files = [x for x in os.listdir(path) if 'Thumb' not in x]
    sorted(files)

    temp = []
    lab: str = ''
    provisional_filename: str = ''

    for file in files:
        yield 1

        if file[:-4][-1] == '1' and len(temp) != 0:
            process(temp, filename=os.path.join(outpath, provisional_filename), dim_x=dim_x, dim_y=dim_y)
            temp.clear()

        if len(temp) == 0:
            lab = file[-10]  # A, B, C in the name

        if file[-10] != lab:
            continue

        # temp.append(files[file])
        provisional_filename = f"{file[:-4][:-3]}_grid"
        temp.append(cv2.imread(os.path.join(path, file)))

    if len(temp) > 1:
        process(temp, os.path.join(outpath, provisional_filename), dim_x, dim_y)

    # time2 = time.time()
    # print(time2-time1)


def fetch_dirs(path: str,
               outpath: str,
               gif: bool = False,
               framerate: int = 1):
    dirs = [os.path.join(path, x) for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
    dirs = sorted(dirs)

    filenames = [x for x in os.listdir(dirs[0]) if 'Thumb' not in x]  # fetch first frames
    print(filenames)

    temp = []
    for f in filenames:
        for d in dirs:
            if f in os.listdir(d):
                temp.append(cv2.imread(os.path.join(d, f)))  # numpy array of frames

        ig = model.ImageGrouper(temp)
        ig.animation(framerate=framerate, gif=gif, filename=os.path.join(outpath, f"{f[:-4]}_stack"))
        temp.clear()
