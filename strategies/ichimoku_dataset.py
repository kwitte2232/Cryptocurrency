#IMPORTS
import pandas as pd
import datetime

#PARAMETERS
columns = ['id','timestamp', 'currency_from', 'currency_to', 'High', 'Low', 'open', 'Close', 'volume', 'quote_volume', 'weighted_ave'] 
ichimoku_params = [9, 26, 52, 22]    
	# [convert_window, base_window, span_B_window, lagging_shift]

#FUNCTIONS
def import_data(url, names):
	'''
	Imports csv as pandas dataframe

	Inputs:
	url: str, dataset 
	names: list, column names

	Returns: pandas dataframe
	'''

	data = pd.read_csv(url, names=names)
	data.index = pd.to_datetime(data['timestamp'], unit='s')
	del data['timestamp']
	del data.index.name
	return data

def find_rolling_highs_and_lows_line(high_data, low_data, window):
	'''
	Find lines like Conversion, Base, and Span B
	
	Inputs:
	high_data: pandas column from dataframe
	low_data: pandas column from dataframe
	window: int, window size
	
	Returns:
	line: single column dataframe
	'''
	
	high = high_data.rolling(window=window).max()
	low = low_data.rolling(window=window).min()
	line = (high + low)/2
	return line.to_frame()

def find_span_B(high_data, low_data, window):
	'''
	Find Span B

	Inputs:
	high_data: pandas column from dataframe
	low_data: pandas column from dataframe
	window: int, window size
	
	Returns:
	span_B: single column dataframe
	'''
	span_B = find_rolling_highs_and_lows_line(high_data, low_data, window).shift(25, freq='min')
	return span_B


def find_span_A(conversion, base):
	'''
	Find Span A

	Inputs:
	conversion: pandas dataframe (conversion line)
	base: pandas dataframe (base line)
	
	Returns:
	span_A: single column dataframe
	'''

	span_A = ((conversion['Conversion'] + base['Base'])/2).shift(25, freq='min')
	return span_A.to_frame()

def find_ichimoku(data, convert_window, base_window, span_B_window, lagging_shift):
	'''
	Find the ichimoku dataset derived from the currency data you want to analyze

	Inputs:
	data: pandas dataframe with the currency data
	convert_window: int, short resolution
	base_window: int, mid-range resolution
	span_B_window: int, long-range resolution
	lagging_shift: int, resolution for back shift
	
	Returns:
	ichimoku: pandas dataframe with Conversion, Base, Span_A, Span_B, and Lagging_Close
	'''

	high_data = data['High']
	low_data = data['Low']
	
	conversion = find_rolling_highs_and_lows_line(high_data, low_data, convert_window)
	conversion = conversion.rename(columns={0:'Conversion'})

	base = find_rolling_highs_and_lows_line(high_data, low_data, base_window)
	base = base.rename(columns={0:'Base'})

	span_B = find_span_B(high_data, low_data, span_B_window)
	span_B = span_B.rename(columns={0:'Span B'})

	span_A = find_span_A(conversion, base)
	span_A = span_A.rename(columns={0:'Span A'})

	lagging = data['Close'].shift(-lagging_shift).to_frame()
	lagging = lagging.rename(columns={'Close':'Lagging Close'})

	measures = [conversion, base, span_B, span_A, lagging]

	ichimoku = pd.concat(measures, axis=1)

	return ichimoku


#MAIN BODY
new_file = '../storage/crypto.csv'
data = import_data(new_file, columns)
data = data.iloc[0:401]   # Cutoff for the dataset
ichimoku = find_ichimoku(data, *ichimoku_params)



