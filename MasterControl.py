import StockData
import CleanData
import PredictionML
import LiveData
import Order
import pandas as pd 



df_HS = StockData.fetchHS('Hour')
print ('Stock Data recived')

df_TrainData = CleanData.fetch_trainData()
print("Training data Fetched")

df_LD = CleanData.fetch_liveData()
print("Live Data Cleaned")


X, y, df = PredictionML.load_and_preprocess_data(df_TrainData)
model, scaler = PredictionML.train_model(X, y)
print("Model Trained")

print(df_LD.dtypes)
latest_data = df_LD
print(df_LD.tail())
live_signal = PredictionML.live_predict(model, scaler, latest_data)
print(live_signal)

last_close = df_LD['Close'].tail()

def order(live_signal):
    match live_signal:
        case 1:
            TP,SL,qty,Limit_price = Order.set_trade_parameters(last_close)
            Order.LimitOrderBuy(Limit_price,qty,TP,SL)
            print("Order placed ")
        case default :
            print ("no Signel is generated")
            

