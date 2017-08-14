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
        self.slope, self.intercept, self.r_value, self.p_value, self.std_err = stats.linregress(test_data['rate'], test_data['timestamp'])

        return self.slope, self.intercept, self.r_value, self.p_value, self.std_err

    def run(self):
        while self.pointer < self.set_length:
            buy = self.testPoint(self.pointer)

            if buy and self.bought == False:
                self.buy(self.data.iloc[self.pointer]['rate'])
            elif buy == False and self.bought:
                self.sell(self.data.iloc[self.pointer]['rate'])

            self.pointer += 1

    def test(self):
        return self.executeStrategy(self.data)

    def testPoint(self, point):
        if point < self.resolution:
            return False

        test_point = point - self.resolution
        test_interval = self.data[test_point:point]

        return self.executeStrategy(test_interval)

    def report(self):
        print self.original_value, self.invested_value

    def reportLine(self):
        return self.slope, self.intercept, self.r_value, self.p_value, self.std_err

    def buy(self, value):
        self.traded_value = float(self.invested_value - self.exchange_fee) / float(value)
        self.bought = True
        self.trades += 1
        self.reportBuy()
        return self.traded_value

    def sell(self, value):
        self.invested_value = float(self.traded_value) * float(value) - self.exchange_fee
        self.bought = False
        self.trades += 1
        self.reportSell()
        return self.invested_value

    def reportBuy(self):
        return None

    def reportSell(self):
        return None






