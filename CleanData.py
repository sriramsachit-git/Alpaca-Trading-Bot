import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt
from datetime import date
import config

# Constants
TICKER = config.TICKER_SYMBOL
today = str(date.today())

def clean_HS():
    # File name
    csvName = "HS_"+TICKER + "_" + today + "_Hour.csv"

    # Read the OHLC data
    df = pd.read_csv(csvName)

    #
    df.reset_index(inplace=True)

    # Rename the required Colums 
    df = df.rename(columns={'open': 'Open'})
    df = df.rename(columns={'low': 'Low'})
    df = df.rename(columns={'close': 'Close'})
    df = df.rename(columns={'high': 'High'})
    df = df.rename(columns={'volume': 'Volume'})

    # Calculate technical indicators using pandas_ta
    bbands = ta.bbands(df['Close'], length=20, std=2)
    df['bb_upper'] = bbands['BBU_20_2.0']
    df['bb_lower'] = bbands['BBL_20_2.0']
    df['bb_percent'] = (df['Close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
    df['RSI'] = ta.rsi(df['Close'], length=14)
    df['Ultimate_Oscillator'] = ta.uo(df['High'], df['Low'], df['Close'], length1=7, length2=14, length3=28)
    df['MFI'] = ta.mfi(df['High'], df['Low'], df['Close'], df['Volume'], length=14)
    return df

# Generate buy and sell signals based on future price movements
def generate_signals(df, future_window=10, profit_threshold=0.02):
    df['Future_Close'] = df['Close'].shift(-future_window)
    df['Return'] = (df['Future_Close'] - df['Close']) / df['Close']
    
    df['Signal'] = 0  # Default to no signal
    df.loc[df['Return'] > profit_threshold, 'Signal'] = 1  # Buy signal
    df.loc[df['Return'] < -profit_threshold, 'Signal'] = -1  # Sell signal
    
    return df

# Clean Historical Data 
df = clean_HS()
# Generate signals
df = generate_signals(df)

# Drop rows with NaN values
df = df.dropna()

# Save the transformed data to a new CSV file
output_csv_name = f'Stock_Signels_{today}.csv'
df.to_csv(output_csv_name, index=False)

print(f"Transformed data saved to '{output_csv_name}'")


if __name__ == "__main__":
    
    # Clean Historical Data 
    df = clean_HS()

    # Generate signals
    df = generate_signals(df)

    # Plot the data
    fig, axs = plt.subplots(3, figsize=(15, 12), sharex=True)

    # Plot the closing price and Bollinger Bands
    axs[0].plot(df['Close'], label='Close', color='blue')
    axs[0].plot(df['bb_upper'], label='BB Upper', linestyle='--', color='red')
    axs[0].plot(df['bb_lower'], label='BB Lower', linestyle='--', color='green')
    axs[0].set_title('Close Price and Bollinger Bands')
    axs[0].legend()

    # Plot RSI
    axs[1].plot(df['RSI'], label='RSI', color='purple')
    axs[1].axhline(70, linestyle='--', color='red')
    axs[1].axhline(30, linestyle='--', color='green')
    axs[1].set_title('Relative Strength Index (RSI)')
    axs[1].legend()

    # Plot signals on the closing price chart
    axs[2].plot(df['Close'], label='Close', color='blue')
    buy_signals = df[df['Signal'] == 1].index
    sell_signals = df[df['Signal'] == -1].index
    axs[2].scatter(buy_signals, df.loc[buy_signals, 'Close'], label='Buy Signal', marker='^', color='green')
    axs[2].scatter(sell_signals, df.loc[sell_signals, 'Close'], label='Sell Signal', marker='v', color='red')
    axs[2].set_title('Buy and Sell Signals')
    axs[2].legend()

    plt.xlabel('Date')
    plt.show()
