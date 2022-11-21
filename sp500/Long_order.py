# 매수 주문
def long_buy_order(buy_price, balances, bal_loc, ticker, df_ticker, atr_value):
    while True:
        # 8000원을 빼고 
        stock_count = int(buy_price // df_ticker.iloc[-1]['Close'])
        buy_price_true = float(stock_count * df_ticker.iloc[-1]['Close'])
        print('종가 = ', df_ticker.iloc[-1]['Close'])
        print('주식 갯수 = ', stock_count)
        print("내가 산 금액 = {:,.0f}달러".format(buy_price_true))
        print("내가 산 주식 명 : {}".format(ticker))
        balances[0]['balance'] = float(balances[0]['balance']) - buy_price_true
        balances[bal_loc]['currency'] = ticker
        balances[bal_loc]['balance'] = float(stock_count)
        balances[bal_loc]['sell_price'] = df_ticker.iloc[-1]['Close'] - (5 * atr_value)
        #샀을때의 가격
        balances[bal_loc]['avg_buy_price'] = float(df_ticker.iloc[-1]['Close'])
        print('매수 체결')
        print('---------------------------------------------')
        return

# 매도 주문
def long_sell_order(balances, bal_loc, ticker, df_ticker):
    while True:
        # 내가 가지고 있는 코인 갯수를 종가와 곱해서 팔았을때의 가격 측정
        print('종가 = ', df_ticker.iloc[-1]['Close'])
        print('주식 갯수 = ', float(balances[bal_loc]['balance']))
        price_cal = df_ticker.iloc[-1]['Close'] * float(balances[bal_loc]['balance'])
        print("내가 판 금액 = {:,.0f}달러".format(price_cal))
        print("내가 판 주식 명 : {}".format(ticker))
        balances[bal_loc]['currency'] = ''
        balances[bal_loc]['balance'] = ''
        balances[bal_loc]['avg_buy_price'] = ''
        balances[bal_loc]['sell_price'] = ''
        # 팔았을 때의 가격을 기존의 지갑잔고에 더하기
        balances[0]['balance'] = balances[0]['balance'] + price_cal
        print('매도 체결')
        print('*** 내 지갑 잔고 = {:,.0f}달러 ***'.format(balances[0]['balance']))
        print('---------------------------------------------')
        return