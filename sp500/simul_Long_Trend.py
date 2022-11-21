import FinanceDataReader as fdr
import time
import datetime
from filter import filter
from atr import ATR
from Long_order import long_sell_order
import pandas_market_calendars as mcal # 영업일 계산 모듈
from func_stock import *

def trading(startyear, startmonth, startday, endyear, endmonth, endday):
    i = 0
    tickers = []
    tickers_rem = []
    balances = []
    # 시작 날짜 입력
    day = datetime.datetime(startyear, startmonth, startday)
    enddate = datetime.datetime(endyear, endmonth, endday)
    # 초기 티커 필터
    endday_change = '{}-{}-{}'.format(day.year, day.month, day.day)
    # 초기 지갑 잔고 입력
    volume = 10000

    balances = ({'currency': 'dolor', 'balance': '{}'.format(volume), 'avg_buy_price': ''}
    , {'currency': '', 'balance': '', 'avg_buy_price': '', 'sell_price': ''} #1
    , {'currency': '', 'balance': '', 'avg_buy_price': '', 'sell_price': ''}
    , {'currency': '', 'balance': '', 'avg_buy_price': '', 'sell_price': ''}
    , {'currency': '', 'balance': '', 'avg_buy_price': '', 'sell_price': ''}
    , {'currency': '', 'balance': '', 'avg_buy_price': '', 'sell_price': ''} # 5
    , {'currency': '', 'balance': '', 'avg_buy_price': '', 'sell_price': ''}
    , {'currency': '', 'balance': '', 'avg_buy_price': '', 'sell_price': ''}
    , {'currency': '', 'balance': '', 'avg_buy_price': '', 'sell_price': ''}
    , {'currency': '', 'balance': '', 'avg_buy_price': '', 'sell_price': ''} # 9 실제 딕셔너리 주소
    , {'currency': '', 'balance': '', 'avg_buy_price': '', 'sell_price': ''})
    empty_count = 9
    assets_total = []
    day_total = []
    while True:
        assets = 0
        while True:
            endday_change = '{}-{}-{}'.format(day.year, day.month, day.day)
            if len(mcal.get_calendar('NYSE').schedule(start_date=endday_change, end_date=endday_change)) == 0:
                print('{} 영업일 아님'.format(endday_change))
                break
            print('---------------------------------------------')
            print(day)
            startday = day - datetime.timedelta(days = 60)
            while True:
                startday_change = '{}-{}-{}'.format(startday.year, startday.month, startday.day)
                endday_change = '{}-{}-{}'.format(day.year, day.month, day.day)
                count = len(mcal.get_calendar('NYSE').schedule(start_date=startday_change, end_date=endday_change))
                if count == 51:
                    break
                startday -= datetime.timedelta(days = 1)

            df = get_ticker_ma(startday_change, endday_change)

            if df.iloc[-1]['MA10'] > df.iloc[-1]['MA25'] and df.iloc[-1]['Close'] > df.iloc[-1]['MA50']:
                
                for k in range(1,11):
                    if balances[k]['currency'] == '':
                        start_filter = True
                        break
                        
                if start_filter == True:
                    tickers_rem = filter(day, endday_change)
                    tickers = []
                start_filter = False

                for i in range(1, 11):
                    tickers_rem.append(balances[i]['currency'])

                # ticker 중복값 제거
                for value in tickers_rem:
                    if value not in tickers:
                        tickers.append(value)

                # 롱 주문
                for j in range(len(tickers)):
                    ticker = tickers[j]
                    for k in range(1, 11):
                        if balances[k]['currency'] == '':
                            empty_count += 1

                    if ticker != '':
                        df_ticker = fdr.DataReader(symbol=ticker, start= startday_change, end=endday_change)
                        atr_value = ATR(day, endday_change, ticker)
                        get_ticker_trade(df_ticker, balances, ticker, atr_value, empty_count)
                        now_price = df_ticker.iloc[-1]['Close']                     # 코인 현재가
                        coin_check = get_balance_stock(balances, ticker) # 코인 보유 하고 있는지 체크
                        balance = coin_check[0][1]                             # 코인 보유 개수
                        if type(balance) == float:
                            assets += now_price * balance
                    empty_count = 0

            elif df.iloc[-1]['MA10'] < df.iloc[-1]['MA25'] or df.iloc[-1]['Close'] < df.iloc[-1]['MA50']:
                # 가지고 있던 코인 팔기
                for j in range(len(tickers)):
                    ticker = tickers[j]
                    if ticker != '':
                        df_ticker = fdr.DataReader(symbol=ticker, start= startday_change, end=endday_change)
                        now_price = df_ticker.iloc[-1]['Close']
                        coin_check = get_balance_stock(balances, ticker)
                        avg_price = coin_check[0][0]
                        bal_loc = coin_check[1]
                        if type(avg_price) == float:
                            long_sell_order(balances, bal_loc, ticker, df_ticker)
                
                print('기다리는중')
            empty_count = 0
            break

        if len(mcal.get_calendar('NYSE').schedule(start_date=endday_change, end_date=endday_change)) != 0:
            assets += float(balances[0]['balance'])
            day_total.append(day)
            assets_total.append(assets)
            print("총 평가 자산 = {:,.0f}달러".format(assets))
            
        # 시간에 24시간씩 계속 추가
        day = day + datetime.timedelta(hours = 24)

        if day == enddate:
            break
        i += 1
        time.sleep(0.2)
