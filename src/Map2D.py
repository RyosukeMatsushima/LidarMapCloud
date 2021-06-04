import numpy as np
import math
from scipy import ndimage
import cv2

from .Axis import Axis
from . import LidarSpec

class Map2D:
    # map resolution means of pixels in 1[m] or 2pi[rad]
    # north angle is 0[rad] and 0 <= angle < 2pi
    # size[m]
    # XY is north east coodinate system
    def __init__(self, map_XY_resolution: int, map_angle_resolution: int, size: int):

        self.XY_resolution = map_XY_resolution
        self.angle_resolution = map_angle_resolution
        self.size = size

        self.pixels_len = map_XY_resolution * size

        # map(angle, X, Y)
        self.data = np.zeros((map_angle_resolution, self.pixels_len, self.pixels_len), dtype=float)
        self._origin_pixel = int(self.pixels_len / 2)

        self.unit_distribution = LidarSpec.UNIT_DISTRIBUTION(map_XY_resolution)
        self.directivity_weight = LidarSpec.DIRECTIVITY_WEIGHT(self.angle_resolution)

    # robot_position: [X, Y]
    # angele[rad]
    # distance[m]
    def add_data(self, robot_position, angle, distance):

        weight = 1
        distance_size = int(LidarSpec.DISTANCE_RESOLUTION(distance) * self.XY_resolution)
        angle_size = int(LidarSpec.ANGLE_RESOLUTION * distance * self.XY_resolution)

        distance_size, angle_size = [4 if value < 4 else value for value in [distance_size, angle_size]]

        distribution = cv2.resize(self.unit_distribution * weight, (distance_size, angle_size))
        distribution = ndimage.rotate(distribution, math.degrees(angle), reshape=True)

        center_distribution = robot_position
        center_distribution[0] += np.cos(angle) * distance
        center_distribution[1] += np.sin(angle) * distance

        directivity_weight = np.roll(self.directivity_weight, self.angle_to_pix(angle))

        #TODO: refactor
        new_distribution = self.adjust_img_to_map(distribution, self.pos_to_pix(center_distribution))
        for i, weight in enumerate(directivity_weight):
            self.data[i] += new_distribution * weight

        return distribution

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
            raise ArithmeticError("out of range")

        return (p0, p1)

    # pos: [X, Y]
    def pos_to_pix(self, pos):
        pix = []
        for i in range(len(pos)):
            pix += [int((pos[i] + self.size / 2) * self.XY_resolution)]
        return pix

    def angle_to_pix(self, angle):
        return int(angle / np.pi * self.angle_resolution)
