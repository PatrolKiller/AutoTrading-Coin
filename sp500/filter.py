import pandas as pd
import FinanceDataReader as fdr
import datetime
import pandas_market_calendars as mcal

def filter(day, endday_change):
    # Step.1 5달러 이하 종목 삭제
    print('※ 5달러 이하 종목 삭제 중 ※')
    sort_list = []
    df_SP500 = fdr.StockListing('SP500')
    tickers = list(df_SP500['Symbol'])
    tickers_5 = []
    
    for i in range(len(tickers)):
        try:
            ticker = tickers[i]
            ticker_now_price = fdr.DataReader(symbol=ticker, start=endday_change, end=endday_change)
            ticker_price = ticker_now_price.iloc[0]['Close']
            if ticker_price > 25:
                tickers_5.append(ticker)
        except:
            pass
    
    print('※ 5달러 이하 종목 삭제 완료 ※')
    sort_list = filter_2(tickers_5, day, endday_change)
    # ticker_5에 5달러 이상 종목 저장
    print(sort_list)
    return sort_list


def filter_2(tickers_5, day, endday_change):
    print(len(tickers_5))
    # Step.2 20일 평균 거래 금액 5,000만달러 이하 삭제
    print('※ 평균 거래 금액 5천만달러 이하 삭제 중 ※')
    j = 0
    sort_list = []
    
    volume_total = pd.DataFrame(columns=['ticker', 'volume'])

    
    startday = day - datetime.timedelta(days = 25)
    while True:
        startday_change = '{}-{}-{}'.format(startday.year, startday.month, startday.day)
        endday_change = '{}-{}-{}'.format(day.year, day.month, day.day)
        count = len(mcal.get_calendar('NYSE').schedule(start_date=startday_change, end_date=endday_change))
        if count == 20:
            break
        startday = startday - datetime.timedelta(days = 1)

    while True:
        # j번째 USDT 종목을 선택한다.
        ticker = tickers_5[j]
        # 티커의 자료를 받는다.
        df = fdr.DataReader(symbol=ticker, start=startday_change, end=endday_change)
        # 이전 ticker의 값 초기화
        dolor_value = []
        dolor_total = 0
        # 하루 거래량 구한다.
        for i in range(len(df)):
            dolor = float(df.iloc[i]['Close']) * float(df.iloc[i]['Volume'])
            dolor_value.append(dolor)
        df.insert(len(df.columns), "dolor", dolor_value)
        # 20일 평균 거래량 구한다.
        for i in range(len(df)):
            dolor_total += df.iloc[i]['dolor']
        dolor_total = int(dolor_total) / 20

        if dolor_total > 250000000:
            volume_total.loc[j] = [ticker, dolor_total]
        j += 1
        if j == len(tickers_5):
            break
    # 인덱스 리셋 (key값 오류뜸)
    volume_total = volume_total.reset_index(drop=True)
    print('※ 평균 거래 금액 5천만달러 이하 삭제 완료 ※')
    sort_list = filter_3(volume_total, day, endday_change)
    return sort_list

def filter_3(volume_total, day, endday_change):
    print(len(volume_total))
    # Step.3 변동률 순위 구하기
    print('※ 변동률 순위 구하는 중 ※')
    # cs를 저장할 데이터 프레임
    j = 0
    USDT_cs = pd.DataFrame(columns=['ticker', 'cs'])

    startday = day - datetime.timedelta(days = 250)
    while True:
        startday_change = '{}-{}-{}'.format(startday.year, startday.month, startday.day)
        endday_change = '{}-{}-{}'.format(day.year, day.month, day.day)
        count = len(mcal.get_calendar('NYSE').schedule(start_date=startday_change, end_date=endday_change))
        if count == 200:
            break
        startday = startday - datetime.timedelta(days = 1)

    while True:
        # j번째 USDT 종목을 선택한다.
        ticker = volume_total.iloc[j]['ticker']
        # 티커의 자료를 받는다.
        df = fdr.DataReader(symbol=ticker, start=startday_change, end=endday_change)
        # cs와 dpc 초기화
        dpc_total = []
        cs_total = []
        for i in range(len(df)):
            # dpc를 추가하는 코드
            if i > 0:
                dpc = (float(df.iloc[i]['Close']) - float(df.iloc[i - 1]['Close']))/float(df.iloc[i-1]['Close'])*100
                dpc_total.append(dpc)
            else:
                dpc = 0
                dpc_total.append(dpc)
        df.insert(len(df.columns), "dpc", dpc_total)
    
        for i in range(len(df)):
            # cs를 추가하는 코드
            if i > 0:
                cs = float(df.iloc[i]['dpc']) + float(cs)
                cs_total.append(cs)
            else:
                cs = 0
                cs_total.append(cs)
        df.insert(len(df.columns), 'cs', cs_total)
    
        # cs값을 절대값으로 구하는 코드
        cs_value = abs(float(df.iloc[len(df)-1]['cs']))
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
