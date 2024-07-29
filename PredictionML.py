import pandas as pd
from datetime import date
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
import CleanData
import matplotlib.pyplot as plt

# Function to load and preprocess data
def load_and_preprocess_data(df):
    # Define the feature columns
    features = [
        'Open', 'High', 'Low', 'Volume', 'trade_count', 'vwap',
        'bb_upper', 'bb_lower', 'bb_percent', 'RSI',
        'Ultimate_Oscillator', 'MFI', 'Close'
    ]
    
    # Drop rows with missing values
    df_temp = df.dropna()
    
    # Separate features (X) and target variable (y)
    X = df_temp[features]
    y = df_temp['Signal']
    
    return X, y, df_temp, features

# Function to train the model
def train_model(X, y):
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Initialize and train the XGBoost classifier
    model = xgb.XGBClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Predict on the test set
    y_pred = model.predict(X_test_scaled)
    
    # Calculate accuracy and classification report
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, zero_division=0)
    
    print(f"Accuracy: {accuracy}")
    print(f"Classification Report:\n{report}")
    
    return model, scaler

# Function to make live predictions
def live_predict(model, scaler, latest_data, features):
    # Scale the latest data
    latest_data_scaled = scaler.transform(latest_data[features])
    
    # Predict using the trained model
    prediction = model.predict(latest_data_scaled)
    
    return prediction

if __name__ == "__main__":
    # Get today's date and construct the input CSV filename
    today = str(date.today())
    input_csv_name = f'Stock_Signals.csv'
    
    # Read the data from the CSV file
    df = pd.read_csv(input_csv_name)
    
    # Load and preprocess the data
    X, y, df, features = load_and_preprocess_data(df)
    print(X.tail())
    
    # Train the model
    model, scaler = train_model(X, y)
    
    # Fetch live data for prediction
    df_temp = CleanData.fetch_liveData()
    
    # Make live predictions
    live_signal = live_predict(model, scaler, df_temp, features)
    print(f"Live prediction: {live_signal}")
