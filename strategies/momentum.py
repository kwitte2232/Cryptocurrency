import numpy
from scipy import stats
import strategy

class Momentum(strategy.Strategy):

    def __init__(self, data):
        self.data = data
        self.setExchangeFee(0)
        self.reset()

    def executeStrategy(self, test_data):

        control_slope = self.getControlLine(test_data)

        test_point = int(round(len(test_data) - self.resolution * 3 / 4))
        test_interval = test_data[test_point:]

        test_slope = self.getLine(test_interval)

        buy = control_slope > self.trade_threshold and test_slope > self.trade_threshold

        return buy

    def getControlLine(self, data):
        self.control_slope, self.control_intercept, self.control_r_value, self.control_p_value, self.control_std_err = self.getLine(data)
        return self.control_slope, self.control_intercept, self.control_r_value, self.control_p_value, self.control_std_err

    def reportControlLine(self):
        return self.control_slope, self.control_intercept, self.control_r_value, self.control_p_value, self.control_std_err
