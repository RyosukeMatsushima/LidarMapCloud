import numpy as np
import math
from scipy import ndimage
import cv2

from . import LidarSpec

class MapElement:

    # Axes X', Y' is rotated around the Z axis from the axes X, Y in north, east system.

    def __init__(self, resolution: int, size: int, angle: float):
        self.resolution = resolution
        self.size = size
        self.angle = angle  # radian
        self._R_to_map = np.array([[np.cos(angle), np.sin(angle)],
                                   [-np.sin(angle), np.cos(angle)]]) #TODO: recheck

        self.pixels_len = resolution * size

        # map(X', Y')
        self.data = np.zeros((self.pixels_len, self.pixels_len), dtype=float)
        self._origin_pixel = int(self.pixels_len / 2)

    def update_map(self, distribution, local_position, AoI): # AoD: angle of incidence
        rotate_angle = AoI - self.angle

        distribution = ndimage.rotate(distribution, math.degrees(rotate_angle), reshape=True)
        pix = self.pos_to_pix(self._R_to_map @ local_position)

        self.data += self.adjust_img_to_map(distribution, pix)

    def adjust_img_to_map(self, img, center_pix):

        #TODO: check img size
        tuples = []
        for i in range(len(img.shape)):
            try:
                tuples += [self.pad_tuple(img.shape[i], self.pixels_len, center_pix[i])]
            except ArithmeticError:
                print("Oops! Img is out of map")

        return np.pad(img, tuples, constant_values=0)

    def pad_tuple(self, now_len: int, to_len: int, center: int):
        p0 = center - int(now_len / 2)
        p1 = to_len - (p0 + now_len)

        if p0 < 0 or p1 > to_len:
            raise ArithmeticError("out of range. Check p0: {} < 0 and p1: {} > to_len: {}".format(p0, p1, to_len))

        return (p0, p1)

    # pos: [X', Y']
    def pos_to_pix(self, pos):
        pix = []
        #TODO: more shorter
        for i in range(len(pos)):
            pix += [int((pos[i] + self.size / 2) * self.resolution)]
        return pix
