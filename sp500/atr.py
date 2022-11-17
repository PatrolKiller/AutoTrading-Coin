import numpy as np
import ccxt
import pandas as pd
import datetime
import FinanceDataReader as fdr
import pandas_market_calendars as mcal

def ATR(day, endday_change, ticker):
    
    startday = day - datetime.timedelta(days = 45)
    while True:
        startday_change = '{}-{}-{}'.format(startday.year, startday.month, startday.day)
        endday_change = '{}-{}-{}'.format(day.year, day.month, day.day)
        count = len(mcal.get_calendar('NYSE').schedule(start_date=startday_change, end_date=endday_change))
        if count == 40:
            break
        startday -= datetime.timedelta(days = 1)
    data = fdr.DataReader(symbol=ticker, start= startday_change, end=endday_change)
    high_low = data['High'] - data['Low']
    high_close = np.abs(data['High'] - data['Close'].shift())
    low_close = np.abs(data['Low'] - data['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr = true_range.rolling(20).sum()/20
    return atr.iloc[-20]