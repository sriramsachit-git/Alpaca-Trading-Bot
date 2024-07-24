import pandas as pd
from datetime import date
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

def load_and_preprocess_data(filename):
    df = pd.read_csv(filename)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    features = [
        'Open', 'High', 'Low', 'Volume', 'trade_count', 'vwap',
        'bb_upper', 'bb_lower', 'bb_percent', 'RSI',
        'Ultimate_Oscillator', 'MFI', 'Return', 'Signal'
    ]
    
    df = df.dropna()
    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    df['Signal'] = df['Signal'].map({-1: 0, 0: 1, 1: 2})
    
    X = df[features]
    y = df['Signal'].shift(-1)
    
    X = X[:-1]
    y = y[:-1]
    
    return X, y, df

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)
    
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

def live_predict(model, scaler, latest_data):
    latest_data_scaled = scaler.transform(latest_data)
    prediction = model.predict(latest_data_scaled)
    return prediction

if __name__ == "__main__":
    today = str(date.today())
    input_csv_name = f'Stock_Signels_{today}.csv'
    
    X, y, df = load_and_preprocess_data(input_csv_name)
    
    model, scaler = train_model(X, y)
    
    X_scaled = scaler.transform(X)
    y_pred_all = model.predict(X_scaled)
    
    # For live prediction, latest_data should be the most recent row(s) of data
    latest_data = X.iloc[-1:].copy()  # Example: get the last row of data
    live_signal = live_predict(model, scaler, latest_data)
    
    print(f"Live prediction: {live_signal}")
