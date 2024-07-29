import StockData
import CleanData
import PredictionML
import LiveData
import Order
import pandas as pd
import time
from datetime import date, datetime, timedelta

today = str(date.today())
# yesterday = str(date.today() - timedelta(days=1))
yesterday = "2018-01-01"

# Set time frame and strategy threshold
timeFrame = "Hour"
startTime = yesterday
endTime = today
TICKER = "BCH/USD"
strategy_threshold = 0.02

# Fetch historical stock data at the specified interval
df_HS = StockData.fetchCrypto(timeFrame, startTime, endTime, TICKER)
print('Stock Data received')

# Fetch the training data
df_TrainData = CleanData.fetch_trainData(df_HS)
print("Training data fetched")

# Load and preprocess the training data
X, y, df, features = PredictionML.load_and_preprocess_data(df_TrainData)
# Train the prediction model and get the scaler
model, scaler = PredictionML.train_model(X, y)
print("Model trained")

# Define the function to place orders based on the live signal
def place_order(live_signal, last_close):
    if live_signal == 1:
        # Set trade parameters (take profit, stop loss, quantity, and limit price)
        TP, SL, qty, Limit_price = Order.set_trade_parameters(last_close)
        # Place a limit buy order
        Order.LimitOrderBuy(Limit_price, qty, TP, SL, TICKER)
        print("Order placed")
    else:
        # Print message if no signal is generated
        print("No signal is generated")

# Start the WebSocket connection in a separate thread for live data updates
websocket_thread = LiveData.run_websocket_in_thread(TICKER)

# Initialize a variable to store the last processed timestamp
last_processed_timestamp = None

while True:
    # Fetch the latest live data
    df_LD = CleanData.fetch_liveData(df)
    
    # Check if there's new data based on the timestamp
    if not df_LD.empty and (last_processed_timestamp is None or df_LD.index[-1] > last_processed_timestamp):
        print("New live data received")
        
        # Update the last processed timestamp
        last_processed_timestamp = df_LD.index[-1]
        
        # Get the latest data point
        latest_data = df_LD.tail(1)
        latest_price = latest_data["Close"].iloc[-1]
        print(f"Latest Price: {latest_price}")
        
        # Predict the live signal using the trained model and scaler
        live_signal = PredictionML.live_predict(model, scaler, latest_data, features)
        print(f"Live signal: {live_signal}")

        # Place order based on the signal
        place_order(live_signal, latest_price)
    
    # Sleep for a short interval before checking for new data again
    time.sleep(2)  # Adjust this value as needed
