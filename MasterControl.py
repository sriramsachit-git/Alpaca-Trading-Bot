import StockData
import CleanData
import PredictionML
import LiveData
import Order
import StocksList
import pandas as pd
import time
from datetime import date, datetime, timedelta

today = str(date.today())
yesterday = str(date.today() - timedelta(days=365))

# Set time frame and strategy threshold
timeFrame = "Hour"
startTime = yesterday
endTime = today
TICKER = StocksList.generatelist()
strategy_threshold = 0.02

# Fetch historical stock data at the specified interval
df_HS = StockData.fetchHS(timeFrame, startTime, endTime, TICKER)
print('Stock Data received')

# Fetch the training data
df_TrainData = CleanData.fetch_trainData(df_HS)
print("Training data fetched")

models = {}
scalers = {}

for symbol, df in df_TrainData.items():
    # Load and preprocess the training data
    X, y, df_temp, features = PredictionML.load_and_preprocess_data(df)
    # Train the prediction model and get the scaler
    model, scaler = PredictionML.train_model(X, y)
    models[symbol] = model
    scalers[symbol] = scaler
    print(f"Model trained for {symbol}")

# Define the function to place orders based on the live signal
def place_order(live_signal, last_close, symbol):
    if live_signal == 1:
        # Set trade parameters (take profit, stop loss, quantity, and limit price)
        TP, SL, qty, Limit_price = Order.set_trade_parameters(last_close)
        # Place a limit buy order
        Order.LimitOrderBuy(Limit_price, qty, TP, SL, symbol)
        print("Order placed")
    else:
        # Print message if no signal is generated
        print("No signal is generated")

# Start the WebSocket connection in a separate thread for live data updates
websocket_thread = LiveData.run_websocket_in_thread(TICKER)

# Initialize a variable to store the last processed timestamp
last_processed_timestamp = {}

while True:
    # Fetch the latest live data
    live_data = CleanData.fetch_liveData(df_HS)
    
    for symbol, df_LD in live_data.items():
        print(f"Processing live data for {symbol}")
        
        # Check if there's new data based on the timestamp
        if not df_LD.empty and (symbol not in last_processed_timestamp or df_LD.index[-1] > last_processed_timestamp[symbol]):
            print(f"New live data received for {symbol}")
            
            # Update the last processed timestamp
            last_processed_timestamp[symbol] = df_LD.index[-1]
            
            # Get the latest data point
            latest_data = df_LD.tail(1)
            latest_price = latest_data["Close"].iloc[-1]
            print(f"Latest Price for {symbol}: {latest_price}")
            
            # Predict the live signal using the trained model and scaler
            live_signal = PredictionML.live_predict(models[symbol], scalers[symbol], latest_data, features)
            print(f"Live signal for {symbol}: {live_signal}")

            # Place order based on the signal
            place_order(live_signal, latest_price, symbol)
    
    # Sleep for a short interval before checking for new data again
    time.sleep(30)  # Adjust this value as needed
