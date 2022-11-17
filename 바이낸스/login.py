# 로그인
import ccxt

def login():

    binance = ccxt.binance({
        #'apiKey' : 'MPe1dhkEUjkk2FEewGDrIOUK5tMKy0f9QhwWNSRYBWjuMQvX2oMb28H4rxf8K5vA',
        #'secret' : 'p26Mb62MBiNutb6M6RYaHGNZCiVUxe92OogQrPBpVEml0nHKuRshcS19Z0HHfkkI',
        'enableRateLimit' : True,
        #'options' : {
        #    'defaultType' : 'future'
        #}
    })
    return binance