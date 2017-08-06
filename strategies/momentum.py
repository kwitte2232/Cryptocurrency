import numpy
from scipy import stats
import strategy

class Momentum(strategy.Strategy):

    def __init__(self, data):
        self.data = list(map(self.extractTimeAndRate, data))
        self.setExchangeFee(0)
        self.reset()

    def testPoint(self, point):
        if point < self.resolution:
            return False

        control_point = point - self.resolution
        control_interval = self.data[control_point:point]

        control_vals = list(map(self.extractRate, control_interval))
        control_times = list(map(self.extractTime, control_interval))
        control_slope = stats.linregress(control_vals, control_times)

        test_point = point - self.resolution / 4
        test_interval = self.data[test_point:point]

        test_vals = list(map(self.extractRate, test_interval))
        test_times = list(map(self.extractTime, test_interval))
        test_slope, intercept, r_value, p_value, std_err = stats.linregress(test_vals, test_times)

        buy = control_slope > self.trade_threshold and test_slope > self.trade_threshold

        if buy and self.bought == False:
            self.buy(self.data[point][1])
        elif buy == False and self.bought:
            self.sell(self.data[point][1])





