import pyupbit
import time
import datetime
from func_stock import Stochastick, get_ticker_trade, CCI

def trade(startyear, startmonth, startday, endyear, endmonth, endday, interval, minutes, ticker):
    # 초기 지갑설정
    balances = []
    day = datetime.datetime(startyear, startmonth, startday)
    endday = datetime.datetime(endyear, endmonth, endday)
    assets = 0
    assets_total = []
    day_total = []
    # 넣을 가격 입력
    volume = 10000000
    balances = ({'currency': 'KRW', 'balance': '{}'.format(volume), 'avg_buy_price': ''}, {
                'currency': '', 'balance': '', 'avg_buy_price': ''})
    while True:
        print_day = day + datetime.timedelta(hours = 9)
        print('\r{}'.format(print_day), end = '')
        df = pyupbit.get_ohlcv(ticker = ticker, interval= interval, to=day)
        df = Stochastick(df, 10, 3, 3)
        df = CCI(df)
        get_ticker_trade(df, balances)
        assets += float(balances[0]['balance'])
        if balances[1]['currency'] != '':
            assets += float(balances[1]['balance'] * balances[1]['avg_buy_price'])
            
        day += datetime.timedelta(minutes=minutes)
        day_total.append(print_day)
        assets_total.append(assets)
        if day == endday:
            break
        assets = 0
        time.sleep(0.1)
    return day_total, assets_total