import unittest
import numpy as np
import matplotlib.pyplot as plt

from src.Map2D import Map2D
from src.Axis import Axis

class Map2DTest(unittest.TestCase):
    def setUp(self):
        print("setUp")
        self.map2D = Map2D(100, 500, 3)

    def test_init(self):
        print("test_init")

        fig = plt.figure(figsize=(10, 3))
        ax = fig.subplots(1, 1)

        ax.imshow(self.map2D.unit_distribution, cmap='gray')
        ax.set_axis_off()
        plt.show()

    def test_add_data(self):
        print("test_add_data")

        for i in range(100):
            angle = 0
            self.map2D.add_data([0, 0], 0, 1)

            if i % 10 == 0:
                fig = plt.figure(figsize=(10, 3))
                ax1, ax2 = fig.subplots(1, 2)

                ax1.imshow(self.map2D.data[self.map2D.angle_to_pix(angle)], cmap='gray')
                d = self.map2D.add_data([0, 0], 2, 1)
                im = ax2.imshow(d, cmap='gray')
                fig.colorbar(im)
                plt.show()

if __name__ == "__main__":
    unittest.main()