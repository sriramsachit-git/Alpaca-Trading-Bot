# Alpaca-Trading-Bot

This repository contains an automated stock trading bot that retrieves historical and live market data, trains an XGBoost model to predict stock movements, and places trades based on these predictions. The bot runs daily before market opens and periodically during the day to ensure timely and accurate trading decisions.


## Features

- Fetches historical and live data

- Implements technical indicators for analysis

- Uses machine learning (XGBoost) for price prediction

- Executes trades automatically through Alpaca API

- Supports real-time data streaming

## Requirements

- Python 3.8+

- pip (Python package manager)

## Installation

1\. Clone this repository:

   ```
   git clone https://github.com/yourusername/crypto-trading-system.git

   cd crypto-trading-system
   ```

2\. Install required packages:

   ```
   pip install -r requirements.txt
   ```

3\. Set up your Alpaca API credentials in `config.py`:

   ```
   API_KEY = 'your_api_key_here'

   SECRET_KEY = 'your_secret_key_here'

   TICKER_SYMBOL = 'BCH/USD'  # or your preferred trading pair
   ```

## Usage

1\. Fetch historical data:

   ```
   python StockData.py
   ```

2\. Clean and prepare data:

   ```
   python CleanData.py
   ```

3\. Train the prediction model:

   ```
   python PredictionML.py

   ```

4\. Run the main trading system:

   ```
   python MasterControl.py
   ```

## File Structure

- `config.py`: Configuration file for API keys and trading pair

- `StockData.py`: Fetches historical cryptocurrency data

- `CleanData.py`: Processes and cleans the data

- `PredictionML.py`: Implements machine learning model for prediction

- `LiveData.py`: Handles real-time data streaming

- `Order.py`: Manages order placement and execution

- `MasterControl.py`: Main script that orchestrates the trading system

## Libraries Used

- pandas: Data manipulation and analysis

- numpy: Numerical computing

- scikit-learn: Machine learning tools

- xgboost: Gradient boosting framework

- matplotlib: Data visualization

- alpaca-trade-api: Alpaca trading API client

- websocket-client: WebSocket client for real-time data

## Disclaimer

This software is for educational purposes only. Use it at your own risk. The authors are not responsible for any financial losses incurred through the use of this system.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/crypto-trading-system/issues) if you want to contribute.



---
