from Long_order import *
import FinanceDataReader as fdr

# 매게변수 ticker 추가 
def get_balance_stock(balances, ticker):
    bool = True
    while True:
        # for문 추가
        for i in range(1, 11):
            if ticker in balances[i]['currency']:
                balance = balances[i]['balance']
                avg_buy_price = balances[i]['avg_buy_price']
                value = (float(avg_buy_price), float(balance))
                bal_loc = int(i)
                bool = False
                break
        if bool == False:
            break
        else:
            pass
        for j in range(1, 11):
            if balances[j]['currency'] == '':
                value = (int(0), int(0))
                bal_loc = int(j)
                bool == False
                break
        if bool == False:
            break
        for k in range(1, 11):
            if balances[j]['currency'] != '':
                value = (str('False'), str('False'))
                bal_loc = str('False')
                break
        break
    return value, bal_loc

# 매게변수 ticker 추가
def get_ticker_trade(df_ticker, balances, ticker, atr_value, empty_count):

    now_price = df_ticker.iloc[-1]['Close']                     # 주식 현재가
    coin_check = get_balance_stock(balances, ticker) # 주식 보유 하고 있는지 체크
    avg_price = coin_check[0][0]                         # 매수 평균가
    balance = coin_check[0][1]                             # 주식 보유 개수
    # 코인의 지갑 위치값 추가
    bal_loc = coin_check[1]
    if type(avg_price) == str:
        return
    print("지갑 위치 = {}".format(bal_loc))
    # 만약 현재가격이 평균가 보다 높아지면 손절매의 가격을 높인다.
    if now_price > avg_price:
        balances[bal_loc]['sell_price'] = now_price - (5 * atr_value)
    # 매수 평균가가 int 이면 매수 조건 체크 float이면 매도 조건 체크
    if type(avg_price) == int:

        # 살 가격 정하기
        # 총자산의 10퍼
        buy_price = float(balances[0]['balance']) / empty_count
        print('{}: '.format(ticker), buy_price)
        long_buy_order(buy_price, balances, bal_loc, ticker, df_ticker, atr_value)
    else:
        # 현재 보유 코인 수익률 계산
        buy_profit = ((now_price - avg_price)/avg_price) * 100
        profit = round(buy_profit, 2)
        if now_price < float(balances[bal_loc]['sell_price']):
            long_sell_order(balances, bal_loc, ticker, df_ticker)
        else:
            print(f"주식명: {ticker}, 수익률: {profit}%")
            print("내가산 가격 = {:,3f}, 시장가격 = {:,3f}".format(avg_price, now_price))
            print('평가 자산 : {:,.0f}달러'.format(float(now_price) * int(balance)))
            print('손절매 가격 {:,.0f}달러'.format(float(balances[bal_loc]['sell_price'])))
            print('---------------------------------------------')

def get_ticker_ma(startday_change, endday_change):
    # S&P500 주가를 넣는다
    ma10 = []
    ma25 = []
    ma50 = []
    df = fdr.DataReader(symbol='US500', start = startday_change, end = endday_change)

    ma10 = df['Close'].rolling(window=10).mean()
    df.insert(len(df.columns), "MA10", ma10)

    ma25 = df['Close'].rolling(window=25).mean()
    df.insert(len(df.columns), "MA25", ma25)

    ma50 = df['Close'].rolling(window=50).mean()
    df.insert(len(df.columns), "MA50", ma50)

    #print('종가: {:,.0f}    ma10: {:,.0f}     ma25: {:,.0f}    ma50: {:,.0f}'.format(df.iloc[-1]['Close'], df.iloc[-1]['MA10'], df.iloc[-1]['MA25'], df.iloc[-1]['MA50']))
    return df