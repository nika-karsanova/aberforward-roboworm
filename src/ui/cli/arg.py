"""
Configuration of Argument Parser object to use as a CLI interface of the application.
"""
import argparse
import os

import src.model.setup as setup


def arg_init():
    """
    Instantiates an arguments parser, which operates with a positional directory argument (directory should contain
    files to be processed for grid or stack) and optional arguments for dimensions of the grid or framerate of the
    animation.
    """

    desc = "\n".join([f"---",
                      f"Welcome to Roboworm Image Processing Application - CLI Interface!",
                      f"To run the merging, please provide input and output paths.",
                      f"Additionally, depending on what type of output you require (stack or grid) provide optional",
                      f"arguments to specify dimensions or framerate with format (GIF or not).",
                      f"If arguments will not be provided, default options will be used.",
                      f"---"])

    p = argparse.ArgumentParser(
        prog='Roboworm Image Grouper',
        description=desc,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    def validate(value):
        if not os.path.isdir(value):
            raise argparse.ArgumentTypeError("Provided directory is not valid. Try again.")

        return value

    p.add_argument('inpath', type=validate, help='Directory to fetch the images from.')
    p.add_argument('outpath', type=validate, help='Directory to output the files into.')

    p.add_argument('-dim', type=int, nargs=2, help='Dimensions of the grid to be made. Defaults to 2x2.',
                   default=(2, 2))

    p.add_argument('-fr', '-framerate', type=int, help='Framerate of the stack to be made. Defaults to 7.',
                   default=7)

    p.add_argument('-g', '-gif', type=bool, help="True, if you want the stack to be made as a GIF. Defaults to True.",
                   default=True)

    args = p.parse_args()

    inpath = args.inpath
    outpath = args.outpath
    grid_mode = setup.inpath_type(inpath)  # returns True if mode is grid

    if grid_mode is None:
        print("Input path invalid. Make sure your path contains files or directories of correct type and try again.")
        p.exit(1)

    files_processed = 0
    total_files = setup.get_total_files(inpath, files=grid_mode, dirs=not grid_mode)
    print_progress_bar(0, total_files, prefix='Progress:', suffix='Complete', length=50)

    if grid_mode:
        x, y = args.dim

        for n in setup.fetch_files(path=inpath,
                                   outpath=outpath,
                                   dim_x=x,
                                   dim_y=y):
            files_processed += n
            print_progress_bar(files_processed, total_files, prefix='Progress:', suffix='Complete', length=50)

    if not grid_mode:
        framerate = args.fr
        is_gif = args.g

        for n in setup.fetch_dirs(path=inpath,
                                  outpath=outpath,
                                  framerate=framerate,
                                  gif=is_gif):
            files_processed += n
            print_progress_bar(files_processed, total_files, prefix='Progress:', suffix='Complete', length=50)


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Credits: Greenstick at https://stackoverflow.com/a/34325723

    Call in a loop to create terminal progress bar.

    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()
