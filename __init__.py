import os
from os.path import dirname, join
import time
import dotenv

import matplotlib.pyplot as plt
import numpy

import gather_data
import strategies.momentum as momentum
import strategies.spike as spike
import strategy_test
import trade

trade = trade.Trade()
trade.run()

time.sleep(1)
