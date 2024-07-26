import StockData
import CleanData
import PredictionML
import LiveData
import Order
import pandas as pd 
import time 


df_HS = StockData.fetchCrypto("Hour")
print ('Stock Data recived')

df_TrainData = CleanData.fetch_trainData()
print("Training data Fetched")

print(df_TrainData.tail())

X, y, df, features = PredictionML.load_and_preprocess_data(df_TrainData)
model, scaler = PredictionML.train_model(X, y)
print("Model Trained")

def order(live_signal,last_close):
    match live_signal:
        case 1:
            TP,SL,qty,Limit_price = Order.set_trade_parameters(last_close)
            Order.LimitOrderBuy(Limit_price,qty,TP,SL)
            print("Order placed ")
        case default :
            print ("no Signel is generated")

# Start the WebSocket connection in a separate thread
websocket_thread = LiveData.run_websocket_in_thread()

# Initialize a variable to store the last processed timestamp
last_processed_timestamp = None

while True:
    # Fetch the latest live data
    df_LD = CleanData.fetch_liveData()
    
    # Check if there's new data
    if not df_LD.empty and (last_processed_timestamp is None or df_LD.index[-1] > last_processed_timestamp):
        print("New live data received")
        
        # Update the last processed timestamp
        last_processed_timestamp = df_LD.index[-1]
        
        # Process the new data
        latest_data = df_LD.tail(1)
        lates_price = df_LD.iloc[-1].at["Close"]
        live_signal = PredictionML.live_predict(model, scaler, latest_data, features)
        print(f"Live signal: {live_signal}")

        
        # Place order based on the signal
        order(live_signal,lates_price)
    
    # Sleep for a short interval before checking for new data again
    time.sleep(2)  # Adjust this value as needed

