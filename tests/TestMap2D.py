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

        im = ax.imshow(np.sum(self.map2D._filter, axis=0), cmap='gray')
        ax.set_axis_off()
        fig.colorbar(im)
        plt.show()

    def test_add_data(self):
        print("test_add_data")

        for i in range(10):
            print(i)
            angle = np.pi / 3
            self.map2D.add_data([0, 0], 0, 0.5)
            self.map2D.add_data([0, 0], angle, 0.5)

        for i, data in enumerate(self.map2D.data):
            if i % 100 == 0:
                angle = i / self.angle_resolution * 2 * np.pi

                fig = plt.figure(figsize=(10, 3))
                ax1, ax2 = fig.subplots(1, 2)

                im = ax1.imshow(data, cmap='gray')
                fig.colorbar(im)
                ax1.set_axis_off()

                ax2.imshow(self.map2D._filter[i], cmap='gray')
                plt.title("{}".format(angle / np.pi * 180))
                plt.show()

        print('likelihood, ad_filter = self.map2D.get_Likelihood_function([0, 0])')
        likelihood, likelihood_polor, ad_filter = self.map2D.get_Likelihood_function([0, 0])

        fig = plt.figure(figsize=(10, 3))
        ax1, ax2 = fig.subplots(1, 2)

        print(likelihood)

        im = ax1.imshow(likelihood, cmap='gray')
        fig.colorbar(im)

        ax2.imshow(likelihood_polor, cmap='gray')
        plt.show()

if __name__ == "__main__":
    unittest.main()