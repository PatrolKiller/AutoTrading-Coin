from order import sell_order, buy_order
from collections import deque
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def get_ticker_trade(df, balances):

    # 코인 종가를 담을 deque 변수
    ma5 = deque(maxlen=5)
    ma20 = deque(maxlen=20)
    ma60 = deque(maxlen=60)

    ma5.extend(df['close'])    # ma5 변수에 종가 넣기
    ma20.extend(df['close'])    # ma20 변수에 종가 넣기
    ma60.extend(df['close'])   # ma60 변수에 종가 넣기

    df['date'] = df.index

    ma5 = df['close'].rolling(window=5).mean()
    df.insert(len(df.columns), "MA5", ma5)

    ma20 = df['close'].rolling(window=20).mean()
    df.insert(len(df.columns), "MA20", ma20)

    #ma60 = df['close'].rolling(window=60).mean()
    #df.insert(len(df.columns), "MA60", ma60)

    now_price = df['close'][-1]       # 코인의 현재가
    coin_check = get_balance_wallet(balances)  # 코인 보유 하고 있는지 체크
    avg_price = coin_check[0]   # 매수 평균가
    balance = coin_check[1]         # 코인 보유 개수

    # 매수 평균가가 int 이면 매수 조건 체크 float이면 매도 조건 체크
    if type(avg_price) == int:
        #df['MA5'][-1] > df['MA20'][-1]
        if df['slow_d'][-1] < df['fast_k'][-1] and df['CCI'][-1] < -50:
            # 살 가격 정하기
            buy_price = float(balances[0]['balance']) * 0.98
            buy_order(df, buy_price, balances)
        else:
            #print('시세 감시 중')
            pass
    else:
        # 현재 보유 코인 수익률 계산
        buy_profit = ((now_price - avg_price)/avg_price) * 100
        profit = round(buy_profit, 2)
        # or df['MA5'][-1] < df['MA20'][-1]
        # df['slow_d_ma'][-1] > df['fast_k_ma'][-1]
        if df['slow_d'][-1] > df['fast_k'][-1]:
            sell_order(df, balances)
        else:
            pass
            #print(f"코인명: ETH, 수익률: {profit}%")
            #print("내가산 가격 = {}, 시장가격 = {}".format(avg_price, now_price))

def get_balance_wallet(balances):
    b = True
    while (b):
        if balances[1]['currency'] == 'ETH':
            balance = balances[1]['balance']
            avg_buy_price = balances[1]['avg_buy_price']
            c = (float(avg_buy_price), float(balance))
            b = False
        else:
            c = (int(0), int(0))
            b = False
    return c

def Stochastick(df, n=10, m=3, t=3):
    ndays_high = df.high.rolling(window=n, min_periods=1).max()
    ndays_low = df.low.rolling(window=n, min_periods=1).min()
    fast_k = ((df.close - ndays_low) / (ndays_high - ndays_low)) * 100
    slow_k = fast_k.ewm(span=m).mean()
    slow_d = slow_k.ewm(span=t).mean()
    df = df.assign(fast_k=fast_k, fast_d=slow_k, slow_k=slow_k, slow_d=slow_d)
    return df

def CCI(df):
    df['AP'] = (df['high'] + df['low'] + df['close']) / 3
    df['SMA'] = df['AP'].rolling(10).mean()
    df['ADV'] = df['AP'].rolling(10).apply(lambda x: pd.Series(x).mad(skipna=True))
    df['CCI'] = (df['AP'] - df['SMA']) / (0.015 * df['ADV'])
    return df
