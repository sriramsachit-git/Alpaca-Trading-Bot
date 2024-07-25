import config
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.enums import OrderSide, QueryOrderStatus
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.requests import LimitOrderRequest, TakeProfitRequest, StopLossRequest
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce
 
API_KEY = config.API_KEY
SECERET_KEY = config.SECRET_KEY
TICKER = config.TICKER_SYMBOL

trading_client = TradingClient(API_KEY, SECERET_KEY, paper=True)

def LimitOrderSell(limit,qty):

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

def LimitOrderBuy(Limit_Price,qty,TP,SL):

    order_request = LimitOrderRequest(
                        symbol=TICKER,             # Replace with your desired symbol
                        qty= qty,                    # Replace with your desired quantity
                        side=OrderSide.BUY,        # Use OrderSide.SELL for selling
                        time_in_force=TimeInForce.GTC,  # Good till cancelled
                        limit_price=Limit_Price,         # Replace with your desired buy price
                        take_profit=TP,
                        stop_loss=SL
)
    # Limit order
    Limit_order = trading_client.submit_order(
                    order_data=order_request)

def CloseAllPositions():
    trading_client.close_all_positions(cancel_orders=True)



def KillSwicth():
    # attempt to cancel all open orders
    cancel_statuses = trading_client.cancel_orders()

def LivePositions():

    # to get all live positions 
    return trading_client.get_all_positions()
    

if __name__ == "__main__":

    market_order_data = MarketOrderRequest(
                    symbol="SPY",
                    qty=0.023,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY
                    )

    # Market order
    market_order = trading_client.submit_order(
                    order_data=market_order_data
               )

    print(LivePositions())