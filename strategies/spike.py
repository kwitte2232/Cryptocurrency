import numpy
from scipy import stats
import strategy

class Spike(strategy.Strategy):

    def __init__(self, data):
        self.data = data
        self.setExchangeFee(0)
        self.reset()

    def executeStrategy(self, test_data):
        self.getLine(test_data)

        buy = self.slope > self.trade_threshold

        return buy






