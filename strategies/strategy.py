from scipy import stats

class Strategy():

    def reset(self):
        self.pointer = 0
        self.set_length = len(self.data)-1

        self.bought = False
        self.invested_value = 0
        self.traded_value = 0
        self.trades = 0

    def setExchangeFee(self, fee):
        self.exchange_fee = fee

    def extractTimeAndRate(self, x):
        return [x[1], x[4]]

    def extractRate(self, x):
        return float(x[1])

    def extractTime(self, x):
        return float(x[0])

    def setResolution(self, resolution):
        self.resolution = resolution

    def setTradeThreshold(self, threshold):
        self.trade_threshold = threshold

    def setInitialInvestment(self, value):
        self.invested_value = value
        self.original_value = value

    def getNet(self):
        return self.invested_value

    def getLine(self, test_data):
        test_vals = list(map(self.extractRate, test_data))
        test_times = list(map(self.extractTime, test_data))

        self.slope, self.intercept, self.r_value, self.p_value, self.std_err = stats.linregress(test_vals, test_times)

        return self.slope, self.intercept, self.r_value, self.p_value, self.std_err

    def run(self):
        while self.pointer < self.set_length:
            buy = self.testPoint(self.pointer)

            if buy and self.bought == False:
                self.buy(self.data[self.pointer][1])
            elif buy == False and self.bought:
                self.sell(self.data[self.pointer][1])

            self.pointer += 1

    def report(self):
        print self.original_value, self.invested_value

    def reportLine(self):
        return self.slope, self.intercept, self.r_value, self.p_value, self.std_err

    def buy(self, value):
        self.traded_value = float(self.invested_value - self.exchange_fee) / float(value)
        self.bought = True
        self.trades += 1
        # print str(value) + " bought."
        return self.traded_value

    def sell(self, value):
        self.invested_value = float(self.traded_value) * float(value) - self.exchange_fee
        self.bought = False
        self.trades += 1
        # print str(value) + " sold. new invested value: " + str(self.invested_value))
        return self.invested_value





