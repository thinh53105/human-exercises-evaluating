

class LowPassFilter:

    def __init__(self, beta):
        self.beta = beta
        self.angle_list = []
        self.filter_list = []
        self.high = True
        self.count = 0

    def cal_next(self, value):
        if not self.angle_list:
            self.angle_list.append(value)
            self.filter_list.append(value - 10)
            return value - 10, -1
        self.angle_list.append(value)
        Fn = self.beta * self.filter_list[-1] + (1 - self.beta) * value
        self.filter_list.append(Fn)
        state = -1
        if self.high and Fn > value:
            self.count += 0.5
            self.high = False
            state = 1
        if not self.high and Fn < value:
            self.count += 0.5
            self.high = True
            state = 0
        return Fn, state

    def reset(self):
        self.high, self.count = True, 0
        self.angle_list = []
        self.filter_list = []