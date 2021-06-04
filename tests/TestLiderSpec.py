import unittest

from src import LidarSpec

class Map2DTest(unittest.TestCase):
    
    def test_DIRECTIVITY_WEIGHT(self):
        print(LidarSpec.DIRECTIVITY_WEIGHT(10))
