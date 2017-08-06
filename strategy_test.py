import matplotlib.pyplot as plt

class StrategyTest():

    def __init__(self, strategy):
        self.strategy = strategy
        self.end = 0
        self.end = 0
        self.interval = 1
        self.results = []

    def setInterval(self, interval):
        if interval >= 1:
            self.interval = interval

    def setRange(self, start, end):
        self.start = start
        self.end = end

    def setPoint(self, point):
        return int(round(point / self.interval))

    def getResults(self):
        return self.results

    def testResolution(self, threshold = 2000, investment = 1000):
        # Set our start and end points in the data
        start = self.setPoint(self.start)
        end = self.setPoint(self.end)

        if start > end:
            # That doesn't work!
            return false

        if start < 1:
            start = 1
        if end < 1:
            end = 1

        for point in range(start, end):
            resolution = point * self.interval
            print "Resolution: " + str(resolution)
            self.runTest(resolution, threshold, investment)

    def testThreshold(self, resolution = 100, investment = 1000):
        # Set our start and end points in the data
        start = self.setPoint(self.start)
        end = self.setPoint(self.end)

        if start > end:
            # That doesn't work!
            return false

        for point in range(start, end):
            threshold = point * self.interval
            print "Threshold: " + str(threshold)
            self.runTest(resolution, threshold, investment)

    def runTest(self, resolution, threshold, investment):
        self.strategy.reset()
        self.strategy.setTradeThreshold(threshold)
        self.strategy.setInitialInvestment(investment)
        self.strategy.setResolution(resolution)
        self.strategy.run()
        self.strategy.report()
        self.results.append(self.strategy.getNet())


    def report(self):
        plt.plot(self.results)
        plt.show()