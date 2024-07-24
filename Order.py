import config
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.enums import OrderSide, QueryOrderStatus
 
API_KEY = config.API_KEY
SECERET_KEY = config.SECRET_KEY
TICKER = config.TICKER_SYMBOL

trading_client = TradingClient(API_KEY, SECERET_KEY, paper=True)

def LimitaOrder(limit,qty):

    limit_order_data = LimitOrderRequest(
                        symbol=TICKER,
                        limit_price=limit,
                        notional=qty,
                        side=OrderSide.SELL,
                        time_in_force=TimeInForce.FOK
                    )

    # Limit order
    limit_order = trading_client.submit_order(
                    order_data=limit_order_data
                )




def KillSwicth():
    # attempt to cancel all open orders
    cancel_statuses = trading_client.cancel_orders()

def LivePositions():

    # to get all live positions 
    trading_client.get_all_positions()