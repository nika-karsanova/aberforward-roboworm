import os

import cv2

import model


def process(temp,
            filename: str = "test",
            dim_x: int = 2,
            dim_y: int = 2):

    print(type(dim_x), dim_x)
    ig = model.ImageGrouper(temp[:dim_x * dim_y])
    ig.grid(size_x=dim_x, size_y=dim_y)
    ig.export_image(filename=filename)


def fetch_files(path: str,
                outpath: str,
                dim_x: int,
                dim_y: int):
    # get files in dir while amending thumbnail variants of images
    files = {x: cv2.imread(os.path.join(path, x)) for x in os.listdir(path) if 'Thumb' not in x}

    temp = []
    lab: str = ''
    provisional_filename: str = ''

    for file in files:
        if file[:-4][-1] == '1' and len(temp) != 0:
            process(temp, filename=os.path.join(outpath, provisional_filename), dim_x=dim_x, dim_y=dim_y)
            temp.clear()

        if len(temp) == 0:
            lab = file[-10]  # A, B, C in the name

        if file[-10] != lab:
            continue

        temp.append(files[file])
        provisional_filename = f"{file[:-4][:-3]}_merged"

    if len(temp) > 1:
        process(temp, os.path.join(outpath, provisional_filename), dim_x, dim_y)


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
        ig.animation(framerate=framerate, gif=gif, filename=os.path.join(outpath, f"{f[:-4]}_anim"))
        temp.clear()
