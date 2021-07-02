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

        self._unit_distribution = LidarSpec.UNIT_DISTRIBUTION(map_XY_resolution)
        self._directivity_weight = LidarSpec.DIRECTIVITY_WEIGHT(self.angle_resolution)

        self._filter, self._filter_size = self.get_filter()

    def get_filter(self):
        lidar_range_pix = int(LidarSpec.RANGE * self.XY_resolution)
        filter_size = lidar_range_pix * 2
        poler_filter = np.zeros((self.angle_resolution, lidar_range_pix), dtype=float)
        map_filter = np.zeros((self.angle_resolution, filter_size, filter_size))

        flags = cv2.INTER_CUBIC + cv2.WARP_FILL_OUTLIERS + cv2.WARP_POLAR_LINEAR + cv2.WARP_INVERSE_MAP

        for angle_pix in range(0, self.angle_resolution):
            poler_filter.fill(0.0)
            poler_filter[angle_pix,:] = 1.0

            map_filter[angle_pix] = cv2.warpPolar(poler_filter, (filter_size, filter_size), (lidar_range_pix, lidar_range_pix), lidar_range_pix, flags)

        return map_filter, filter_size

    # robot_position: [X, Y]
    # angele[rad]
    # distance[m]
    def add_data(self, robot_position, angle, distance):

        weight = 1
        distance_size = int(LidarSpec.DISTANCE_RESOLUTION(distance) * self.XY_resolution)
        angle_size = int(LidarSpec.ANGLE_RESOLUTION * distance * self.XY_resolution)

        distance_size, angle_size = [4 if value < 4 else value for value in [distance_size, angle_size]]

        distribution = cv2.resize(self._unit_distribution * weight, (angle_size, distance_size))
        distribution = ndimage.rotate(distribution, math.degrees(angle), reshape=True)

        center_distribution = robot_position
        center_distribution[0] += np.cos(angle) * distance
        center_distribution[1] += np.sin(angle) * distance

        directivity_weight = np.roll(self._directivity_weight, self.angle_to_pix(angle))

        #TODO: refactor
        ajusted_distribution = self.adjust_img_to_map(distribution, self.pos_to_pix(center_distribution))
        for i, weight in enumerate(directivity_weight):
            self.data[i] += ajusted_distribution * weight

        return distribution

    def get_Likelihood_function(self, robot_position):
        tuples = [ (0, 0) ]

        for robot_pix in self.pos_to_pix(robot_position):
            try:
                tuples += [ self.pad_tuple(self._filter_size, self.pixels_len, robot_pix) ]
            except ArithmeticError as error:
                print(error)

        print(tuples)
        ajusted_filter = np.pad( self._filter, tuples, constant_values=0 )
        print(ajusted_filter.shape)
        likelihood_poler = np.sum( self.data * ajusted_filter, axis=0 )

        return likelihood_poler, ajusted_filter

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

    # pos: [X, Y]
    def pos_to_pix(self, pos):
        pix = []
        #TODO: more shorter
        for i in range(len(pos)):
            pix += [int((pos[i] + self.size / 2) * self.XY_resolution)]
        return pix

    def angle_to_pix(self, angle):
        return int(angle / np.pi * self.angle_resolution)
