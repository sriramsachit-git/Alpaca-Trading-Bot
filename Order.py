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

def set_trade_parameters(entry_price):
    
    take_profit_percentage = 2.0  # Preset take profit percentage
    stop_loss_percentage = 1.0     # Preset stop loss percentage

    take_profit_price = entry_price * (1 + take_profit_percentage / 100)
    stop_loss_price = entry_price * (1 - stop_loss_percentage / 100)
    stop_loss_limit_price = stop_loss_price - 1.0  # Example stop limit price adjustment

    take_profit_request = TakeProfitRequest(limit_price=take_profit_price)
    stop_loss_request = StopLossRequest(stop_price=stop_loss_price, limit_price=stop_loss_limit_price)

    return take_profit_request, stop_loss_request

def set_trade_parameters(entry_price):
    allocated_budget = 1000
    take_profit_percentage = 2.0  # Preset take profit percentage
    stop_loss_percentage = 1.0     # Preset stop loss percentage

    # Calculate take profit and stop loss prices
    take_profit_price = entry_price * (1 + take_profit_percentage / 100)
    stop_loss_price = entry_price * (1 - stop_loss_percentage / 100)
    stop_loss_limit_price = stop_loss_price - 1.0  # Example stop limit price adjustment

    # Determine limit price (1% more than entry price)
    limit_price = entry_price * (1 + 1.0 / 100)

    # Calculate the quantity of shares that can be bought with the allocated budget
    quantity = int(allocated_budget / limit_price)

    # Create requests
    take_profit_request = TakeProfitRequest(limit_price=take_profit_price)
    stop_loss_request = StopLossRequest(stop_price=stop_loss_price, limit_price=stop_loss_limit_price)

    return take_profit_request, stop_loss_request, quantity, limit_price


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