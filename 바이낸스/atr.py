import numpy as np
import ccxt
import pandas as pd
import login

binance = login.login()

def ATR(day, interval, ticker):
    data = binance.fetch_ohlcv(symbol = ticker, since = day, limit= 40, timeframe = interval)
    data = pd.DataFrame(data, columns = ['date', 'open', 'high', 'low', 'close', 'volume'])
    high_low = data['high'] - data['low']
    high_close = np.abs(data['high'] - data['close'].shift())
    low_close = np.abs(data['low'] - data['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr = true_range.rolling(20).sum()/20
    return atr.iloc[-20]