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

        

if __name__ == "__main__":
    unittest.main()