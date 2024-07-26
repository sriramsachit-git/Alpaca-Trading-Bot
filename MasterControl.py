import StockData
import CleanData
import PredictionML
import LiveData
import Order
import pandas as pd 
import time 

# Fetch historical stock data at an hourly interval
df_HS = StockData.fetchCrypto("Hour")
print('Stock Data received')

# Fetch the training data
df_TrainData = CleanData.fetch_trainData()
print("Training data fetched")

# Load and preprocess the training data
X, y, df, features = PredictionML.load_and_preprocess_data(df_TrainData)
# Train the prediction model and get the scaler
model, scaler = PredictionML.train_model(X, y)
print("Model trained")

# Define the function to place orders based on the live signal
def order(live_signal, last_close):
    match live_signal:
        case 1:
            # Set trade parameters (take profit, stop loss, quantity, and limit price)
            TP, SL, qty, Limit_price = Order.set_trade_parameters(last_close)
            # Place a limit buy order
            Order.LimitOrderBuy(Limit_price, qty, TP, SL)
            print("Order placed")
        case default:
            # Print message if no signal is generated
            print("No signal is generated")

# Start the WebSocket connection in a separate thread for live data updates
websocket_thread = LiveData.run_websocket_in_thread()

# Initialize a variable to store the last processed timestamp
last_processed_timestamp = None

while True:
    # Fetch the latest live data
    df_LD = CleanData.fetch_liveData()
    
    # Check if there's new data based on the timestamp
    if not df_LD.empty and (last_processed_timestamp is None or df_LD.index[-1] > last_processed_timestamp):
        print("New live data received")
        
        # Update the last processed timestamp
        last_processed_timestamp = df_LD.index[-1]
        
        # Get the latest data point
        latest_data = df_LD.tail(1)
        latest_price = df_LD.iloc[-1].at["Close"]
        # Predict the live signal using the trained model and scaler
        live_signal = PredictionML.live_predict(model, scaler, latest_data, features)
        print(f"Live signal: {live_signal}")

        # Place order based on the signal
        order(live_signal, latest_price)
    
    # Sleep for a short interval before checking for new data again
    time.sleep(2)  # Adjust this value as needed
