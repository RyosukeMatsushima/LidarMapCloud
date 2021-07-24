import unittest
import numpy as np
import cv2
import matplotlib.pyplot as plt

from src.MapElement import MapElement
from src import LidarSpec

class MapElementTestCase(unittest.TestCase):
    def setUp(self):
        print("setUp")
        self.resolution = 100
        self.size = 3
        self.mapElement1 = MapElement(self.resolution, 3, 0)
        self.mapElement2 = MapElement(self.resolution, 3, 0)
        self.mapElement3 = MapElement(self.resolution, 3, 0)

        self.mapElement1_1 = MapElement(self.resolution, 3, 0)
        self.mapElement1_2 = MapElement(self.resolution, 3, np.pi / 10)
        self.mapElement1_3 = MapElement(self.resolution, 3, np.pi / 2)

    def test_init(self):
        print("test_init")

    def test_update_map(self):
        distribution = LidarSpec.UNIT_DISTRIBUTION(self.resolution)
        distribution = cv2.resize(distribution, (4, 100))

        position = np.array([1., 0.])
        self.mapElement1.update_map(distribution, position, 0)
        position = np.array([0., 1.])
        self.mapElement2.update_map(distribution, position, np.pi / 10)
        position = np.array([0., -1.])
        self.mapElement3.update_map(distribution, position, np.pi / 2)
        self._show_img(self.mapElement1.data)
        self._show_img(self.mapElement2.data)
        self._show_img(self.mapElement3.data)

        position = np.array([1., 0.])
        self.mapElement1_1.update_map(distribution, position, 0)
        position = np.array([1., 0.])
        self.mapElement1_2.update_map(distribution, position, 0)
        position = np.array([1., 0.])
        self.mapElement1_3.update_map(distribution, position, 0)
        self._show_img(self.mapElement1_1.data)
        self._show_img(self.mapElement1_2.data)
        self._show_img(self.mapElement1_3.data)


    def _show_img(self, img):
        fig = plt.figure(figsize=(10, 3))
        ax = fig.subplots(1, 1)

        im = ax.imshow(img, cmap='gray')
        ax.set_axis_off()
        fig.colorbar(im)
        plt.show()


