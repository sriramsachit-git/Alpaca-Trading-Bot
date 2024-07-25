import StockData
import CleanData
import PredictionML
import LiveData
import pandas as pd 



df_HS = StockData.fetchHS('Hour')
print ('Stock Data recived')

df_TrainData = CleanData.fetch_trainData(df_HS)
print("Training data Fetched")

df_LD = CleanData.fetch_liveData(df_HS)
print("Live Data Cleaned")


X, y, df = PredictionML.load_and_preprocess_data(df_HS)
model, scaler = PredictionML.train_model(X, y)
print("Model Trained")

latest_data = df_LD
live_signal = PredictionML.live_predict(model, scaler, latest_data)
print(live_signal)


