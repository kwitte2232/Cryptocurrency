import numpy
from scipy import stats
import strategy

class Spike(strategy.Strategy):

    def __init__(self, data):
        self.data = list(map(self.extractTimeAndRate, data))
        self.setExchangeFee(0)
        self.reset()

        self.good_trades = []
        self.bad_trades = []

    def testPoint(self, point):
        if point < self.resolution:
            return False

        test_point = point - self.resolution
        test_interval = self.data[test_point:point]

        return self.testData(test_interval)

    def test(self):
        return self.testData(self.data)

    def testData(self, test_data):
        self.getLine(test_data)

        buy = self.slope > self.trade_threshold

        return buy





