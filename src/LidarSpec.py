import numpy as np
from scipy.stats import multivariate_normal

ANGLE_RESOLUTION = 0.01 # [rad]

RANGE = 1 # [m]

def DISTANCE_RESOLUTION(distance):
    return distance * 0.01

def UNIT_DISTRIBUTION(map_XY_resolution: int):

    VARIANCE = 0.06

    axis = np.linspace(-0.5, 0.5, map_XY_resolution + 1, endpoint=True)
    x, y = np.meshgrid(axis, axis)
    pos = np.dstack((x, y))
    rv = multivariate_normal([0, 0], [[VARIANCE, 0], [0, VARIANCE]])
    return rv.pdf(pos)

def DIRECTIVITY_WEIGHT(angle_resolution):

    THRESHOLD = 0

    directivity_weight = np.array([np.cos(point / angle_resolution * 2 * np.pi) for point in range(angle_resolution)])
    directivity_weight = np.where(directivity_weight < THRESHOLD, 0, directivity_weight)

    return directivity_weight
