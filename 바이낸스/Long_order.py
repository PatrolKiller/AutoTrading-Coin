# 매수 주문
def long_buy_order(buy_price, balances, bal_loc, ticker, df):
    while True:
        # 8000원을 빼고 
        print("내가 산 금액 = {:,.0f}원".format(buy_price))
        print("내가 산 코인 명 : {}".format(ticker))
        balances[0]['balance'] = float(balances[0]['balance']) - buy_price
        balances[bal_loc]['currency'] = ticker
        # 8000원을 종가로 나누어 코인갯수 구하기
        balances[bal_loc]['balance'] = float(buy_price / df.iloc[-1]['close'])
        #샀을때의 가격
        balances[bal_loc]['avg_buy_price'] = float(df.iloc[-1]['close'])
        print('매수 체결')
        print('---------------------------------------------')
        return

# 매도 주문
def long_sell_order(balances, bal_loc, ticker, df):
    while True:
        # 내가 가지고 있는 코인 갯수를 종가와 곱해서 팔았을때의 가격 측정
        print('종가 = ', df.iloc[-1]['close'])
        print('코인 갯수 = ', float(balances[bal_loc]['balance']))
        price_cal = df.iloc[-1]['close'] * float(balances[bal_loc]['balance'])
        print("내가 판 금액 = {:,.0f}원".format(price_cal))
        print("내가 판 코인 명 : {}".format(ticker))
        balances[bal_loc]['currency'] = ''
        balances[bal_loc]['balance'] = ''
        balances[bal_loc]['avg_buy_price'] = ''
        # 팔았을 때의 가격을 기존의 지갑잔고에 더하기
        balances[0]['balance'] = balances[0]['balance'] + price_cal
        print('매도 체결')
        print('*** 내 지갑 잔고 = {:,.0f}원 ***'.format(balances[0]['balance']))
        print('---------------------------------------------')
        return