import numpy
from scipy import stats
import strategy

class Spike(strategy.Strategy):

    def __init__(self, data):
        self.data = list(map(self.extractTimeAndRate, data))
        self.setExchangeFee(0)
        self.reset()

    def testPoint(self, point):
        if point < self.resolution:
            return False

        test_point = point - self.resolution
        test_interval = self.data[test_point:point]

        test_vals = list(map(self.extractRate, test_interval))
        test_times = list(map(self.extractTime, test_interval))

        slope, intercept, r_value, p_value, std_err = stats.linregress(test_vals, test_times)

        buy = slope > self.trade_threshold and std_err < slope

        if buy and self.bought == False:
            self.buy(self.data[point][1])
        elif buy == False and self.bought:
            self.sell(self.data[point][1])





