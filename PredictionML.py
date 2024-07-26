import pandas as pd
from datetime import date
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
import CleanData
import matplotlib.pyplot as plt

def load_and_preprocess_data(df):
    features = ['Open', 'High', 'Low', 'Volume', 'trade_count', 'vwap',
        'bb_upper', 'bb_lower', 'bb_percent', 'RSI',
        'Ultimate_Oscillator', 'MFI', 'Close']
    df_temp = df.dropna()
    X = df[features]
    y = df['Signal']
    print("df load_and_preprocess_data")
    print(df.tail())
    return X, y, df_temp, features

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, random_state=42, shuffle=False)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    model = xgb.XGBClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    print(f"Accuracy: {accuracy}")
    print(f"Classification Report:\n{report}")
    return model, scaler

def live_predict(model, scaler, latest_data, features):
    latest_data_scaled = scaler.transform(latest_data[features])
    prediction = model.predict(latest_data_scaled)
    return prediction

if __name__ == "__main__":
    today = str(date.today())
    input_csv_name = f'Stock_Signals_{today}.csv'
    df = pd.read_csv(input_csv_name)
    X, y, df, features = load_and_preprocess_data(df)
    print(X.tail())
    model, scaler = train_model(X, y)
    
    # For live prediction, latest_data should be the most recent row(s) of data
    df_temp = CleanData.fetch_liveData()

    live_signal = live_predict(model, scaler, df_temp, features)
    print(f"Live prediction: {live_signal}")
   
