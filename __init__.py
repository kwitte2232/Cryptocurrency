import os
from os.path import dirname, join
import time
import dotenv

import gather_data

dotenv.load_dotenv(join(dirname(__file__), '.env'))

DATA_RESOLUTION = os.environ.get('DATA_RESOLUTION')

btceth = gather_data.GatherData('BTC', 'ETH')

# print(gather_data.pull_result(str(int(time.time())), 'BTC', 'ETH'))
btceth.schedule_rate_pulls(interval=DATA_RESOLUTION)

time.sleep(1)

# print btceth.retrieve_exchange_rates()
