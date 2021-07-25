import numpy as np
import math
from scipy import ndimage
import cv2

from .MapElement import MapElement
from . import LidarSpec

class LidarData:
    def __init__(self, position, angle, distance):
        self.position = position
        self.angle = angle
        self.distance = distance

class Map2D:
    # map resolution means of pixels in 1[m] or 2pi[rad]
    # north angle is 0[rad] and 0 <= angle < 2pi
    # size[m]
    # XY is north east coodinate system
    def __init__(self, map_XY_resolution: int, map_angle_resolution: int, size: int):

        self.XY_resolution = map_XY_resolution
        self.angle_resolution = map_angle_resolution
        self.size = size

        # map data as list of MapElement
        self.data = [ MapElement(map_XY_resolution, size, angle) for angle in range(map_angle_resolution) ]
        self.lider_data = []    # [LidarDistance1, ...]

        self._unit_distribution = LidarSpec.UNIT_DISTRIBUTION(map_XY_resolution)
        self._directivity_weight = LidarSpec.DIRECTIVITY_WEIGHT(self.angle_resolution)

    # robot_position: [X, Y]
    # angele[rad]
    # distance[m]
    def add_data(self, robot_position, angle, distance):
        self.lider_data += [LidarData(position, angle, distance)]

    def update_map(self):
        distance_size = int(LidarSpec.DISTANCE_RESOLUTION(distance) * self.XY_resolution)
        angle_size = int(LidarSpec.ANGLE_RESOLUTION * distance * self.XY_resolution)

        distance_size, angle_size = [4 if value < 4 else value for value in [distance_size, angle_size]]

        distribution = cv2.resize(self._unit_distribution, (angle_size, distance_size))

        directivity_weight = np.roll(self._directivity_weight, self.angle_to_pix(angle))

        for i, element in enumerate(self.data):
            weight = directivity_weight[i]
            [ element.update_map(distribution * weight, ) for data in self.lider_data ]

        for data in self.lider_data:
            [ element.update_map(distribution, data.position, data.angle) for element in self.data ]


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

        flags = cv2.INTER_CUBIC + cv2.WARP_FILL_OUTLIERS + cv2.WARP_POLAR_LINEAR + cv2.WARP_INVERSE_MAP
        likelihood = cv2.warpPolar(likelihood_poler, (self.angle_resolution, self.pixels_len), (self._origin_pixel, self._origin_pixel), self.pixels_len, flags)

        return likelihood, likelihood_poler, ajusted_filter

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
