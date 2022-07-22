import argparse
import os

from model import fetch_files

"""
Configuration of Argument Parser object to use as a CLI interface of the application.
"""


def arg_init():
    """
    Instantiates an arguments parser, which operates with a positional directory argument (directory should contain
    files to be processed for grid or stack) and optional arguments for dimensions of the grid or framerate of the
    animation.
    """

    p = argparse.ArgumentParser(
        prog='Roboworm Image Grouper',
        description='An application to assistant image analysis from the Roboworm platform.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    def validate(value):
        if not os.path.isdir(value):
            raise argparse.ArgumentTypeError("Provided directory is not valid. Try again.")

        return value

    p.add_argument('directory', type=validate, help='Directory to fetch the images from.')
    p.add_argument('outpath', type=validate, help='Directory to output the files into.')
    p.add_argument('-dim', type=int, nargs=2, help='Dimensions of the grid to be made.')
    p.add_argument('-fr', '-framerate', type=int, help='Framerate of the stack to be made.')

    args = p.parse_args()

    # TODO: depending on dir structure, verify whether dim or fr is provided
    directory = args.directory
    outpath = args.outpath
    x, y = args.dim
    framerate = args.fr


