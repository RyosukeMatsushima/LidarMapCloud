import numpy as np

class Axis:
    def __init__(self, name, min, max, resolution):
        self.name = name
        self.min = min
        self.max = max
        self.resolution = resolution
        self.elements = np.arange(min, max + resolution, resolution)
        self.steps = np.full(self.elements.shape[0], resolution, dtype=float) #TODO: update step

    def num2val(self, num):
        self.check_num_range(num)
        return self.elements[num]

    def val2num(self, val):
        self.check_val_range(val)
        return np.abs(self.elements - val).argmin()

    def check_num_range(self, num):
        if num < 0 or len(self.elements) < num:
            raise ArithmeticError("num is not in range")

    def check_val_range(self, val):
        if val < self.min - self.resolution/2 or self.max + self.resolution/2 < val:
            print(val)
            raise ArithmeticError("val is not in range")

    def get_step(self, num):
        return self.steps[num]

    def get_param(self):
        return {"name": self.name, "min": self.min, "max": self.max, "resolution": self.resolution}
