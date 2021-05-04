import numpy as np
from scipy.stats import multivariate_normal

ANGLE_RESOLUTION = 0.01 # [rad]

def DISTANCE_RESOLUTION(distance):
    return distance * 0.01

def UNIT_DISTRIBUTION(map_XY_resolution: int):

    DISTANCE_VARIANCE = 0.06
    ANGLE_VARIANCE = 0.06

    axis = np.linspace(-0.5, 0.5, map_XY_resolution + 1, endpoint=True)
    x, y = np.meshgrid(axis, axis)
    pos = np.dstack((x, y))
    rv = multivariate_normal([0, 0], [[DISTANCE_VARIANCE, 0], [0, ANGLE_VARIANCE]])
    return rv.pdf(pos)
