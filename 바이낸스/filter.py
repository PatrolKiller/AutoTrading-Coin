import login
import pandas as pd
binance = login.login()

def filter(day, interval):
    # Step.1 5달러 이하 종목 삭제
    print('※ 5달러 이하 종목 삭제 중 ※')
    sort_list = []
    markets = binance.fetch_tickers() #선물거래 load_markets()
    markets = pd.DataFrame(markets)
    tickers = []
    tickers_5 = []
    for i in range(len(markets.columns)):
        if "/USDT" in markets.iloc[0][i]:
            ticker = markets.iloc[0][i]
            tickers_5.append(ticker)
    # 선물 거래 코드
    # markets = markets.drop(['BTCSTUSDT', 'BTCUSDT_220930', 'ETHUSDT_220930', 'UNFI/USDT'],axis=1)
    # markets = markets.reset_index(drop=True)
    # tickers = []
    # tickers_5 = []
    # for i in range(len(markets.columns)):
    #     if "/USDT" in markets.iloc[1][i]:
    #         ticker = markets.iloc[1][i]
    #         tickers.append(ticker)
    for i in range(len(tickers)):
        ticker = tickers[i]
        ticker_now_price = binance.fetch_ohlcv(symbol = ticker, since = day, limit= 1, timeframe = interval)
        ticker_now_price = pd.DataFrame(ticker_now_price, columns = ['date', 'open', 'high', 'low', 'close', 'volume'])
        # ticker_now_price = binance.fetch_ticker(ticker) #실제 거래 코드
        # ticker_price = ticker_now_price['close'] #실제 거래 코드
        ticker_price = ticker_now_price.iloc[0]['close']
        if ticker_price > 5:
            tickers_5.append(ticker)
    print('※ 5달러 이하 종목 삭제 완료 ※')
    sort_list = filter_2(tickers_5, day, interval)
    # ticker_5에 5달러 이상 종목 저장
    return sort_list

def filter_2(tickers_5, day, interval):
    # Step.2 20일 평균 거래 금액 5,000만달러 이하 삭제
    print('※ 평균 거래 금액 5천만달러 이하 삭제 중 ※')
    j = 0
    sort_list = []
    volume_total = pd.DataFrame(columns=['ticker', 'volume'])
    while True:
        # j번째 USDT 종목을 선택한다.
        ticker = tickers_5[j]
        # 티커의 자료를 받는다.
        df = binance.fetch_ohlcv(symbol = ticker, since = day, limit= 20, timeframe = interval)
        df = pd.DataFrame(df, columns=['date', 'open',
                      'high', 'low', 'close', 'volume'])
        # 이전 ticker의 값 초기화
        dolor_value = []
        dolor_total = 0
        # 하루 거래량 구한다.
        for i in range(len(df)):
            dolor = float(df.loc[i, 'close']) * float(df.loc[i, 'volume'])
            dolor_value.append(dolor)
        df.insert(len(df.columns), "dolor", dolor_value)
        # 20일 평균 거래량 구한다.
        for i in range(len(df)):
            dolor_total += df.loc[i, 'dolor']
        dolor_total = int(dolor_total)
        if dolor_total > 50000000:
            volume_total.loc[j] = [ticker, dolor_total]
        j += 1
        if j == len(tickers_5):
            break
    # 인덱스 리셋 (key값 오류뜸)
    volume_total = volume_total.reset_index(drop=True)
    print('※ 평균 거래 금액 5천만달러 이하 삭제 완료 ※')
    sort_list = filter_3(volume_total, day, interval)
    return sort_list

def filter_3(volume_total, day, interval):
    # Step.3 변동률 순위 구하기
    print('※ 변동률 순위 구하는 중 ※')
    # cs를 저장할 데이터 프레임
    j = 0
    USDT_cs = pd.DataFrame(columns=['ticker', 'cs'])
    while True:
        # j번째 USDT 종목을 선택한다.
        ticker = volume_total.loc[j, 'ticker']
        # 티커의 자료를 받는다.
        df = binance.fetch_ohlcv(symbol = ticker, since = day, limit= 200, timeframe = interval)
        # cs와 dpc 초기화
        dpc_total = []
        cs_total = []
        df = pd.DataFrame(df, columns=['date', 'open',
                      'high', 'low', 'close', 'volume'])
        for i in range(len(df)):
            # dpc를 추가하는 코드
            if i > 0:
                dpc = (float(df.loc[i, 'close']) - float(df.loc[i -
                   1, 'close']))/float(df.loc[i-1, 'close'])*100
                dpc_total.append(dpc)
            else:
                dpc = 0
                dpc_total.append(dpc)
        df.insert(len(df.columns), "dpc", dpc_total)
    
        for i in range(len(df)):
            # cs를 추가하는 코드
            if i > 0:
                cs = float(df.loc[i, 'dpc']) + float(cs)
                cs_total.append(cs)
            else:
                cs = 0
                cs_total.append(cs)
        df.insert(len(df.columns), 'cs', cs_total)
    
        # cs값을 절대값으로 구하는 코드
        cs_value = abs(float(df.loc[len(df)-1, 'cs']))
        USDT_cs.loc[j] = [ticker, cs_value]
        j += 1
        if j == len(volume_total):
            break
    USDT_cs_sort = USDT_cs.sort_values('cs', ascending=False)
    USDT_cs_sort = USDT_cs_sort.reset_index(drop=True)
    sort_list = []
    for sort in range(10):
        sort_list.append(USDT_cs_sort.iloc[sort][0])
    print('※ 변동률 순위 구하기 완료 ※')
    return sort_list
