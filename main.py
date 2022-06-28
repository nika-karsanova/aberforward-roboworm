"""
This is the main module of the IBERS Image Merger program.
It is responsible for setting up the main module and configuring the behaviour of the program.

The main outputs can be categorized into multiple groups:

    - (N/2) x (N/2) grid images out of N given photos, where N is an even number between [2..10]
    - a continuous horizontal merge of N images, where N is number of images between [2..10]
    - animations, consisting out of N provided images, where N is number of images between [2..100]

"""

__author__ = 'Nika Karsanova'
__email__ = 'vek2@aber.ac.uk'

import PIL
import os
import cv2
import numpy as np

from PIL import Image

path = "C:/Users/welleron/Desktop/aberworks/june/aberforward/samples/tif_samples"
# path = "C:/Users/welleron/Desktop/pers/bg"


def opencv_animation():
    frames = [cv2.imread(os.path.join(path, x)) for x in os.listdir(path)]

    widths, heights = zip(*(i.shape[:2] for i in frames))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter('video.mp4', fourcc, 7, (max(widths), max(heights)))

    for f in frames:
        writer.write(f)

    cv2.destroyAllWindows()
    writer.release()


def opencv_tiles():
    images = [cv2.imread(os.path.join(path, x)) for x in os.listdir(path)]

    merged_images = []  # top and bottom

    for i in range(0, 4, 2):
        heights, widths = zip(*(i.shape[:2] for i in [images[i], images[i+1]]))

        merged_image = np.zeros((max(heights), sum(widths), 3), dtype=np.uint8)
        merged_image[:, :] = (255, 255, 255)

        offset = images[i].shape[1]
        merged_image[:images[i].shape[0], :offset, :3] = images[i]

        merged_image[:images[i+1].shape[0], offset:offset+images[i+1].shape[1], :3] = images[i+1]

        merged_images.append(merged_image)

    merged_heights, merged_widths = zip(*(i.shape[:2] for i in merged_images))

    full_image = np.zeros((sum(merged_heights), max(merged_widths), 3), dtype=np.uint8)

    f_offset = merged_images[0].shape[0]

    full_image[:f_offset, :merged_images[0].shape[1], :3] = merged_images[0]
    full_image[f_offset:f_offset+merged_images[1].shape[0], :merged_images[1].shape[1]] = merged_images[1]

    cv2.imwrite("test.png", full_image)


def opencv_horizontal():
    images = [cv2.imread(os.path.join(path, x)) for x in os.listdir(path)]

    heights, widths = zip(*(i.shape[:2] for i in images))

    merged_image = np.zeros((max(heights), sum(widths), 3), dtype=np.uint8)
    merged_image[:, :] = (255, 255, 255)

    offset = images[0].shape[1]

    merged_image[:images[0].shape[0], :offset, :3] = images[0]

    for i in range(1, len(images)):
        merged_image[:images[i].shape[0], offset:offset + images[i].shape[1], :3] = images[i]
        offset += images[i].shape[1]

    cv2.imwrite("test.png", merged_image)


def pil():
    images = [PIL.Image.open(os.path.join(path, x)) for x in os.listdir(path)]

    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    merged_image = PIL.Image.new('L', (total_width, max_height))

    x_offset = 0
    for image in images:
        merged_image.paste(image, (x_offset, 0))
        x_offset += image.size[0]

    merged_image.save('test.png', "PNG")


def main():
    # pil()
    opencv_animation()


if __name__ == '__main__':
    main()
