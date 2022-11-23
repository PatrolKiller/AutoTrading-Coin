def buy_order(df, buy_price, balances):
    while True:
        # 8000원을 빼고
        balances[0]['balance'] = float(balances[0]['balance']) - buy_price
        balances[1]['currency'] = 'ETH'
        # 8000원을 종가로 나누어 코인갯수 구하기
        balances[1]['balance'] = float(buy_price / df['close'][-1])
        #샀을때의 가격
        balances[1]['avg_buy_price'] = float(df['close'][-1])
        #print('매수 체결')
        return
        
def sell_order(df, balances):
    while True:
        # 내가 가지고 있는 코인 갯수를 종가와 곱해서 팔았을때의 가격 측정
        sell_price = df['close'][-1] * (balances[1]['balance'])
        balances[1]['currency'] = ''
        balances[1]['balance'] = ''
        balances[1]['avg_buy_price'] = ''
        # 팔았을 때의 가격을 기존의 지갑잔고에 더하기
        balances[0]['balance'] = balances[0]['balance'] + sell_price * 0.9998
        #print('매도 체결')
        #print('내 지갑 잔고 = {:,.0f}원'.format(balances[0]['balance']))
        return        