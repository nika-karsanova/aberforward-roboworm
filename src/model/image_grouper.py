from typing import List

import cv2
import numpy as np
from PIL import Image


class ImageGrouper:
    """
    This is the ImageGrouper module of the IBERS Image Merger program.
    It contains a class that is responsible for the main functionality of the program.
    Utilises Pillow, OpenCV, NumPy to perform required image and animation manipulations.
    Allows to export image as a binary for display in GUI or as a image or video file (e.g., png).
    """

    def __init__(self,
                 files: List[np.ndarray]):
        """
        Function that initialises the ImageGrouper object based on the given files.
        Files are loaded in as NumPy arrays to allow for work with files of formats such as TIF and RAW.

        :param files: List of NumPy array which represent the files to be processed.
        """

        self.files = files
        self.imgs = [Image.fromarray(img) for img in self.files]
        self.merged_image: Image = Image
        # self.data = io.BytesIO()

    def unite(self,
              images: list[Image]):  # makes strips of given PIL images
        """
        Function that merges given PIL Image objects horizontally.

        :param images: PIL Image objects derived from numpy arrays
        """

        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths)
        max_height = max(heights)

        self.merged_image = Image.new('L', (total_width, max_height))

        x_offset = 0
        for image in images:
            self.merged_image.paste(image, (x_offset, 0))
            x_offset += image.size[0]

    def strip(self):
        """
        Function to encapsulate the horizontal merging functionality of the program.
        Performs a check on number of images.
        """
        assert 10 >= len(self.imgs) >= 2, "Number of images is not sufficient"

        self.unite(self.imgs)
        # self.merged_image.save(self.data, 'png')

    def grid(self,
             size_x: int = 2,
             size_y: int = 2):

        """
        Function to generate a tiles (grid) image palette from the loaded in files.
        Dimension of the image is required for successful generation, defaults to a 2x2 grid.

        :param size_x: number of columns
        :param size_y: number of rows
        """

        assert len(self.imgs) == size_x * size_y, "Number of images selected does not match number of images required"

        wip: list = []  # stores work in progress images

        offset = 0
        for _ in range(size_x):  # generate top image, bottom image etc.
            self.unite(self.imgs[offset:offset + size_x])  # makes image row
            wip.append(self.merged_image)
            offset += size_x  # shift offset

        # build final image
        widths, heights = zip(*(i.size for i in wip))
        max_width = max(widths)
        total_height = sum(heights)

        self.merged_image = Image.new('L', (max_width, total_height))  # make the final image

        y_offset = 0
        for i in range(size_y):
            self.merged_image.paste(wip[i], (0, y_offset))
            y_offset += wip[i].size[1]

        # self.merged_image.save(self.data, 'png')

    def animation(self,
                  framerate: int = 7,
                  gif: bool = False,
                  filename: str = 'video'):
        """

        :param framerate: specified framerate to generate video or gif with, defaults to 7.
        :param gif: whether or not the user selected option of generating a gif.
        :param filename: custom filename.
        """
        if gif:
            self.imgs[0].save(f"{filename}.gif",
                              save_all=True,
                              append_images=self.imgs[1:],
                              duration=framerate,
                              loop=0,
                              )

        else:
            widths, heights = zip(*(i.shape[:2] for i in self.files))  # can't use PIL Image objects to make an mp4

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # codec of mp4 format

            writer = cv2.VideoWriter(f"{filename}.mp4",
                                     fourcc,
                                     framerate,
                                     (max(widths), max(heights)),
                                     )

            for f in self.files:  # create animation
                writer.write(f)

            cv2.destroyAllWindows()
            writer.release()

    def export_image(self,
                     filename: str = 'image'):
        """
        Exports the resulting image in PNG format.

        :param filename: custom filename
        """
        self.merged_image.save(f"{filename}.png", "PNG")
