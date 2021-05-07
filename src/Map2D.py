import numpy as np
import math
from scipy import ndimage
import cv2

from .Axis import Axis
from . import LidarSpec

class Map2D:
    # map resolution is number of pixels in 1[m] or 2pi[rad]
    # size[m]
    def __init__(self, map_XY_resolution: int, map_angle_resolution: int, size: int):

        self.XY_resolution = map_XY_resolution
        self.angle_resolution = map_angle_resolution

        self.pixels_len = map_XY_resolution * size

        # map(angle, X, Y)
        self.data = np.zeros((map_angle_resolution, self.pixels_len, self.pixels_len), dtype=float)
        self._origin_pixel = int(self.pixels_len / 2)

        self.unit_distribution = LidarSpec.UNIT_DISTRIBUTION(map_XY_resolution)

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

        self.data[self.angle_to_pix(angle)] += self.adjust_img_to_map(distribution, self.pos_to_pix(center_distribution))

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
            pix += [int(pos[i] / self.XY_resolution) + self._origin_pixel]
        
        return pix

    def angle_to_pix(self, angle):
        return int(angle / self.angle_resolution)

    # def __init__(self, axisX: Axis, axisY: Axis, axisTheta: Axis, axisDistance: Axis):
    #     self.axisX = axisX
    #     self.axisY = axisY
    #     self.axisTheta = axisTheta
    #     self.axisDistance = axisDistance

    #     filename = path.join(mkdtemp(), 'likelihood_data.dat')
    #     self.likelihood_data = np.memmap(filename, dtype='float32', mode='w+', shape=(len(axisX.elements), len(axisY.elements), len(axisTheta.elements), len(axisDistance.elements)))

    #     filename = path.join(mkdtemp(), 'data_count.dat')
    #     self.data_count = np.memmap(filename, dtype='int64', mode='w+', shape=(len(axisX.elements), len(axisY.elements)))

    #     self._scan_data_set = [] # [[X, Y, angle, distance, weight]] of robot

    #     self.normal_diffusion = self.get_normal_diffusion()

    # def get_normal_diffusion(self):
    #     return np.random.normal(0, 1, (400, 2)) * np.array([LidarSpec.ANGLE_RESOLUTION, LidarSpec.DISTANCE_RESOLUTION(1.)])

    # def add_data(self, X, Y, angle, distance, weight):
    #     self._scan_data_set.append(X, Y, angle, distance, weight])

    # def calculate_likelihood_around(self, X, Y):

    # def calculate_likelihood(self, X, Y):
    #     pos = np.array([X, Y])
    #     num_X = self.axisX.val2num(X)
    #     num_Y = self.axisY.val2num(Y)
    #     for scan_data in self._scan_data_set[self.data_count[num_X][num_Y]:]:
    #         scan_pos = np.array([scan_data[0], scan_data[1]])
    #         angle = scan_data[2]
    #         distance = scan_data[3]
    #         weight = scan_data[4]

    #         angle2scanner = np.acos()
