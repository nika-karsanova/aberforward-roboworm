"""
    This is the ImageGrouper module of the IBERS Image Merger program.
    It contains a class that is responsible for the main functionality of the program.
    Utilises Pillow, OpenCV, NumPy to perform required image and animation manipulations.
    Allows to export image as a binary for display in GUI or as a image or video file (e.g., png).
    """

import cv2
import numpy as np
from PIL import Image


class ImageGrouper:
    """
    Class that combines all the functionality to merge images or animations for files provided.

    Two variants of the implementation are provided: one using Pillow, another using NumPy.
    NumPy is significantly quicker, but Pillow variants are left for reference.
    """

    def __init__(self,
                 files: list[np.ndarray]):
        """
        Function that initialises the ImageGrouper object based on the given files.
        Files are loaded in as NumPy arrays to allow for work with files of formats such as TIF and RAW.

        :param files: List of NumPy array which represent the files to be processed.
        """

        self.files = files
        self.imgs = [Image.fromarray(img) for img in self.files]
        self.merged_image: np.ndarray = np.ndarray([])
        # self.data = io.BytesIO()

    def unite_pil_variant(self,
                          images: list[Image]):

        """
        Function that merges given PIL Image objects horizontally.
        Works off PILLOW.

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

    def unite(self,
              images: list[np.ndarray]):  # makes strips of given PIL images
        """
        Function that merges given numpy arrays horizontally, creating required image.
        Works off NumPy.

        :param images: numpy arrays to create an image from
        """

        heights, widths = zip(*(i.shape[:2] for i in images))

        self.merged_image = np.zeros((max(heights), sum(widths), 3), dtype=np.uint8)
        self.merged_image[:, :] = (255, 255, 255)

        offset = images[0].shape[1]

        self.merged_image[:images[0].shape[0], :offset, :3] = images[0]

        for i in range(1, len(images)):
            self.merged_image[:images[i].shape[0], offset:offset + images[i].shape[1], :3] = images[i]
            offset += images[i].shape[1]

    def grid_pil_variant(self,
                         size_x: int = 2,
                         size_y: int = 2
                         ):

        """
        Function to generate a tiles (grid) image palette from the loaded in files.
        Dimension of the image is required for successful generation, defaults to a 2x2 grid.
        Works off PILLOW.

        :param size_x: number of columns
        :param size_y: number of rows
        """

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

    def grid(self,
             size_x: int = 2,
             size_y: int = 2):

        """
        Function to generate a tiles (grid) image palette from the loaded in files.
        Dimension of the image is required for successful generation, defaults to a 2x2 grid.
        Works of NumPy.

        :param size_x: number of columns
        :param size_y: number of rows
        """

        # assert len(self.imgs) == size_x * size_y, "Number of images selected does not match number of images required"

        wip: list = []  # stores work in progress images

        offset = 0
        for _ in range(size_x):  # generate top image, bottom image etc.
            self.unite(self.files[offset:offset + size_x])  # makes image row
            wip.append(self.merged_image)
            offset += size_x  # shift offset

        merged_heights, merged_widths = zip(*(i.shape[:2] for i in wip))

        self.merged_image = np.zeros((sum(merged_heights), max(merged_widths), 3), dtype=np.uint8)

        f_offset = wip[0].shape[0]

        self.merged_image[:f_offset, :wip[0].shape[1], :3] = wip[0]
        self.merged_image[f_offset:f_offset + wip[1].shape[0], :wip[1].shape[1]] = wip[1]

    def animation(self,
                  framerate: int = 7,
                  gif: bool = False,
                  filename: str = 'video'):
        """
        Creates a so-called stack of images (animation) in GIF or MP4 formats.

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
        cv2.imwrite(f"{filename}.png", self.merged_image)

    def export_image_pil_variant(self,
                                 filename: str = 'image'):

        """
        Exports the resulting image in PNG format.
        PILLOW variant.

        :param filename: custom filename
        """
        self.merged_image.save(f"{filename}.png", "PNG")
