import unittest

from src.Axis import Axis

class TestAxis(unittest.TestCase):
    def setUp(self):
        self.axis_name = "test_name"
        self.min = -2.4
        self.max = 3.2
        self.step = 0.2
        self.axis = Axis(self.axis_name, self.min, self.max, self.step)

    def test_num2val(self):
        resolution = 100000000
        self.assertTrue(abs(self.axis.num2val(4) - (self.min + self.step * 4)) < 1/resolution)
    
    def test_val2num(self):
        print("test_val2num")
        num = 5
        self.assertEqual(self.axis.val2num(self.min + self.step * num), num)


if __name__ == "__main__":
    unittest.main()