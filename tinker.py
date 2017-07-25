import dotenv
import os
from os.path import dirname, join
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import exchange_rate

dotenv.load_dotenv(join(dirname(__file__), '.env'))

DATA_RESOLUTION = os.environ.get('DATA_RESOLUTION')

rates = exchange_rate.ExchangeRate().fetchAll()

price_data = []

for rate in rates:
    price_data.append([int(rate[1]), float(rate[4])])

plt.plot(price_data)

# 0.0817
# 0.08067064