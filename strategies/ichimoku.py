from __future__ import division
import numpy
from scipy import stats
import strategy
import matplotlib.pyplot as plt
import pandas as pd

class Ichimoku(strategy.Strategy):

    def __init__(self, data):
        self.data = data
        self.setExchangeFee(0)
        self.reset()

    def executeStrategy(self, test_data):
        self.last_index = test_data.iloc[-1].name
        # print last_index

        params = [9, 26, 52, 22]   # [convert_window, base_window, span_B_window, lagging_shift]
        ichimoku = self.findIchimoku(test_data, *params)
        # self.plot(ichimoku, test_data)

        test_frame = ichimoku.loc[self.last_index]

        self.conversion = test_frame['conversion']
        self.base = test_frame['base']
        self.span_a = test_frame['span_a']
        self.span_b = test_frame['span_b']

        # True = green cloud, False = red cloud
        cloud_trend = self.span_a > self.span_b
        # The cloud is big
        cloud_threshold = self.span_a / self.span_b > self.trade_threshold / 10000
        # Tenkan is above the Kijun
        line_trend = self.conversion > self.base
        # Tenkan is above the cloud
        line_cloud_trend = self.conversion > self.span_a and self.conversion > self.span_b

        # Either Tenkan is above the Kijun with a green cloud, or the cloud is red but we've already bought
        buy = (line_trend and cloud_trend and line_cloud_trend and cloud_threshold) or (line_trend and line_cloud_trend and self.bought)

        # print buy
        # if buy: print self.last_index

        return buy

    def plot(self, ichimoku, test_data):

        column_names = list(ichimoku.columns)
        fig = plt.figure()
        ax1 = fig.add_subplot(111, ylabel='ETH Price in BTC')

        colors = ['blue', 'cyan', 'red', 'green']
        for col, color in zip(column_names, colors):
            if col not in ['lagging_close', 'timestamp']:
                ax1.plot(ichimoku.index, ichimoku[col], label=col, color=color)

        ax1.plot(test_data.index, test_data.close, linestyle=':', label="Close Price", color='k')

        # Fill the clouds

        a = ichimoku['span_a']
        b = ichimoku['span_b']

        plt.fill_between(ichimoku.index, a, b, where=a >= b, facecolor='green', alpha='0.2', interpolate=True)
        plt.fill_between(ichimoku.index, a, b, where=b >= a, facecolor='red', alpha='0.2', interpolate=True)

        ax1.legend(bbox_to_anchor=(1.5, 1.05))
        plt.xticks(rotation='vertical')

        print ichimoku.describe()
        plt.show()

    # Conversion Line

    def findRollingHighsAndLowsLine(self, high_data, low_data, window):
        '''
        Can be used to find conversion line or base line depending on the window size
        
        Inputs:
        high_data: pandas column from dataframe
        low_data: pandas column from dataframe
        window: int, window size
        
        Returns:
        line: 
        '''
        
        high = high_data.rolling(window=window).max()
        low = low_data.rolling(window=window).min()
        line = (high + low)/2

        return line.to_frame()

    def findSpanB(self, high_data, low_data, window):
        span_B = findRollingHighsAndLowsLine(high_data, low_data, window).shift(25, freq='min')
        return span_B

    def findSpanA(self, conversion, base):
        span_a = ((conversion['conversion'] + base['base'])/2).shift(25, freq='min')

        return span_a.to_frame()

    def findIchimoku(self, data, convert_window, base_window, span_b_window, lagging_shift):
        high_data = data['high']
        low_data = data['low']
        timestamp = data['timestamp']
        
        conversion = self.findRollingHighsAndLowsLine(high_data, low_data, convert_window)
        conversion = conversion.rename(columns={0:'conversion'})

        base = self.findRollingHighsAndLowsLine(high_data, low_data, base_window)
        base = base.rename(columns={0:'base'})

        span_b = self.findSpanB(high_data, low_data, span_b_window)
        span_b = span_b.rename(columns={0:'span_b'})

        span_a = self.findSpanA(conversion, base)
        span_a = span_a.rename(columns={0:'span_a'})

        lagging = data['close'].shift(-lagging_shift).to_frame()
        lagging = lagging.rename(columns={'close':'lagging_close'})

        measures = [timestamp, conversion, base, span_b, span_a, lagging]

        ichimoku = pd.concat(measures, axis=1)

        ichimoku.index = pd.to_datetime(ichimoku['timestamp'], unit='s')
        del ichimoku.index.name

        return ichimoku

    # def reportBuy(self):
    #     print self.last_index, self.span_a / self.span_b
    #     self.bought_value = self.invested_value
    #     self.bought_rate = self.data.iloc[self.pointer]['rate']

    # def reportSell(self):
    #     print self.last_index, self.bought_value <= self.invested_value, self.bought_value, self.invested_value, self.invested_value - self.bought_value





