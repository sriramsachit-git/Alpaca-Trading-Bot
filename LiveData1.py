from alpaca_trade_api.common import URL
from alpaca_trade_api.stream import Stream

import config

API_KEY = config.API_KEY
SECRET_KEY = config.SECRET_KEY

async def trade_callback(t):
    print('trade', t)


async def quote_callback(q):
    print('quote', q)


# Initiate Class Instance
stream = Stream(API_KEY,
               SECRET_KEY,
                base_url=URL('https://paper-api.alpaca.markets'),
                data_feed='iex')  # <- replace to 'sip' if you have PRO subscription

# subscribing to event
stream.subscribe_trades(trade_callback, 'AAPL')
stream.subscribe_quotes(quote_callback, 'IBM')

stream.run()