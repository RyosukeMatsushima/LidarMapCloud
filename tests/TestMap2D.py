import unittest
import numpy as np
import matplotlib.pyplot as plt

from src.Map2D import Map2D
from src.Axis import Axis

class Map2DTest(unittest.TestCase):
    def setUp(self):
        print("setUp")
        self.xy_resolution = 100
        self.angle_resolution = 500
        self.map2D = Map2D(self.xy_resolution, self.angle_resolution, 3)

    def test_init(self):
        print("test_init")

        fig = plt.figure(figsize=(10, 3))
        ax = fig.subplots(1, 1)

        ax.imshow(self.map2D.unit_distribution, cmap='gray')
        ax.set_axis_off()
        plt.show()

    def test_add_data(self):
        print("test_add_data")

        for i in range(10):
            angle = np.pi / 2
            self.map2D.add_data([0, 0], 0, 1)
            self.map2D.add_data([0, 0], angle, 1)

        for i, data in enumerate(self.map2D.data):
            if i % 10 == 0:
                angle = i / self.angle_resolution * 2 * np.pi

                fig = plt.figure(figsize=(10, 3))
                ax = fig.subplots(1, 1)

                im = ax.imshow(data, cmap='gray')
                fig.colorbar(im)
                ax.set_axis_off()
                plt.title("{}".format(angle / np.pi * 180))
                plt.show()

if __name__ == "__main__":
    unittest.main()