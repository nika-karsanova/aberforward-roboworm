from typing import List

import PIL
import cv2
import numpy as np
import imageio
from PIL import Image
import io


class ImageGrouper:
    def __init__(self,
                 files: List[np.ndarray]):

        self.files = files
        self.imgs = [Image.fromarray(img) for img in self.files]
        self.merged_image: Image = Image
        self.data = io.BytesIO()

    def unite(self, images: list[Image]):  # makes strips of given PIL images
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths)
        max_height = max(heights)

        self.merged_image = Image.new('L', (total_width, max_height))

        x_offset = 0
        for image in images:
            self.merged_image.paste(image, (x_offset, 0))
            x_offset += image.size[0]

    def strip(self):
        assert 10 >= len(self.imgs) >= 2, "Number of images is not sufficient"

        self.unite(self.imgs)
        self.merged_image.save(self.data, 'png')

    def grid(self, size_x: int = 2, size_y: int = 2):

        assert len(self.imgs) == size_x * size_y, "Number of images selected does not match number of images required"

        wip: list = []  # stores work in progress images

        offset = 0

        for _ in range(size_x):  # generate top image, bottom image etc.
            self.unite(self.imgs[offset:offset + size_x])  # makes image row
            wip.append(self.merged_image)
            offset += size_x  # shift offset

        widths, heights = zip(*(i.size for i in wip))
        max_width = max(widths)
        total_height = sum(heights)

        self.merged_image = Image.new('L', (max_width, total_height))  # make the final image

        y_offset = 0
        for i in range(size_y):
            self.merged_image.paste(wip[i], (0, y_offset))
            y_offset += wip[i].size[1]

        self.merged_image.save(self.data, 'png')

    def animation(self, gif: bool = False):
        if gif:
            self.imgs[0].save('anim.gif', save_all=True, append_images=self.imgs[1:], duration=7, loop=0)

        else:
            widths, heights = zip(*(i.shape[:2] for i in self.files))

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter('video.mp4', fourcc, 7, (max(widths), max(heights)))

            for f in self.files:
                writer.write(f)

            cv2.destroyAllWindows()
            writer.release()

    def export_image(self, filename: str = 'test.png'):
        self.merged_image.save(filename, "PNG")
