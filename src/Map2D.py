import numpy as np

from .Axis import Axis
from . import LidarSpec

class Map2D:
    # map resolution is number of pixels in 1[m] or 2pi[rad]
    # size[m]
    def __init__(self, map_XY_resolution: int, map_angle_resolution: int, size: int):

        pixels_XY = map_XY_resolution * size

        # map(angle, X, Y)
        self.map = np.zeros((map_angle_resolution, pixels_XY, pixels_XY), dtype=float)
        self._origin_pixel = int((int(size / 2) + 1 / 2) * map_XY_resolution)

        self.unit_distribution = np.zeros((pixels_XY, pixels_XY), dtype=float)
        mark1 = int(size / 2) * map_XY_resolution
        mark2 = mark1 + map_XY_resolution + 1
        self.unit_distribution[mark1 : mark2, mark1 : mark2] = LidarSpec.UNIT_DISTRIBUTION(map_XY_resolution)

    def set_data(self, robot_position, angle, distance):
        return



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
