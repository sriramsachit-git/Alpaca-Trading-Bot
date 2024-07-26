import config
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.enums import OrderSide, QueryOrderStatus
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.requests import LimitOrderRequest, TakeProfitRequest, StopLossRequest
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce

# Load API keys and ticker symbol from config file
API_KEY = config.API_KEY
SECERET_KEY = config.SECRET_KEY
TICKER = config.TICKER_SYMBOL

# Initialize the Alpaca trading client in paper trading mode
trading_client = TradingClient(API_KEY, SECERET_KEY, paper=True)

# Function to place a limit sell order
def LimitOrderSell(limit, qty):
    limit_order_data = LimitOrderRequest(
        symbol=TICKER,
        limit_price=limit,
        notional=qty,
        side=OrderSide.SELL,
        time_in_force=TimeInForce.FOK
    )

    # Submit the limit sell order
    limit_order = trading_client.submit_order(order_data=limit_order_data)

# Function to place a limit buy order with take profit and stop loss
def LimitOrderBuy(Limit_Price, qty, TP, SL):
    order_request = LimitOrderRequest(
        symbol=TICKER,
        qty=qty,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.GTC,  # Good till cancelled
        limit_price=Limit_Price,
        take_profit=TP,
        stop_loss=SL
    )

    # Submit the limit buy order
    Limit_order = trading_client.submit_order(order_data=order_request)

# Function to set trade parameters (take profit, stop loss, quantity, and limit price)
def set_trade_parameters(entry_price):
    allocated_budget = 1000
    take_profit_percentage = 2.0  # Preset take profit percentage
    stop_loss_percentage = 1.0    # Preset stop loss percentage

    # Calculate take profit and stop loss prices
    take_profit_price = entry_price * (1 + take_profit_percentage / 100)
    stop_loss_price = entry_price * (1 - stop_loss_percentage / 100)
    stop_loss_limit_price = stop_loss_price - 1.0  # Example stop limit price adjustment

    # Determine limit price (1% more than entry price)
    limit_price = entry_price * (1 + 1.0 / 100)

    # Calculate the quantity of shares that can be bought with the allocated budget
    quantity = int(allocated_budget / limit_price)

    # Create take profit and stop loss requests
    take_profit_request = TakeProfitRequest(limit_price=take_profit_price)
    stop_loss_request = StopLossRequest(stop_price=stop_loss_price, limit_price=stop_loss_limit_price)

    return take_profit_request, stop_loss_request, quantity, limit_price

# Function to close all positions and cancel all open orders
def CloseAllPositions():
    trading_client.close_all_positions(cancel_orders=True)

# Function to cancel all open orders
def KillSwicth():
    cancel_statuses = trading_client.cancel_orders()

# Function to get all live positions
def LivePositions():
    return trading_client.get_all_positions()

# Main execution block
if __name__ == "__main__":
    # Create a market order request to buy a small quantity of SPY
    market_order_data = MarketOrderRequest(
        symbol="SPY",
        qty=0.023,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY
    )

    # Submit the market order
    market_order = trading_client.submit_order(order_data=market_order_data)

    # Print all live positions
    print(LivePositions())
