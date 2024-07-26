import pandas as pd
import pandas_ta as ta
from datetime import date
import config
import plotly.graph_objects as go
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Constants
TICKER = config.TICKER_SYMBOL
today = str(date.today())

# File name
csvName = "HS_" + "BTC" + "_" + today + "_Hour.csv"
# Read the OHLC data
df = pd.read_csv(csvName)

def clean_LD():
    # File name
    csvName = "LiveData.csv"
    # Read the OHLC data
    df = pd.read_csv(csvName)
    # Adding timestamp
    df = df.rename(columns={'t': 'timestamp'})
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    # Rename the required Columns 
    df = df.rename(columns={'o': 'Open', 'l': 'Low', 'c': 'Close', 'h': 'High', 'v': 'Volume'})

    return df

def clean_HS():
    # File name
    csvName = "HS_" + "BTC" + "_" + today + "_Hour.csv"
    # Read the OHLC data
    df = pd.read_csv(csvName)
    
    # Adding timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True) 

    # Rename the required Columns
    df = df.rename(columns={'open': 'Open', 'low': 'Low', 'close': 'Close', 'high': 'High', 'volume': 'Volume'})
   
    print("Historical Data Recived")
    return df

def concat_data(df_ld, df_hs):#Some Technical Indicators need more values to be caluclated 
    df = pd.concat([df_hs, df_ld])
    return df

def TA_Data(df):
    # Calculate technical indicators using pandas_ta
    bbands = ta.bbands(df['Close'], length=20, std=2)
    df['bb_upper'] = bbands['BBU_20_2.0']
    df['bb_lower'] = bbands['BBL_20_2.0']
    df['bb_percent'] = (df['Close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
    df['RSI'] = ta.rsi(df['Close'], length=14)
    df['Ultimate_Oscillator'] = ta.uo(df['High'], df['Low'], df['Close'], length1=7, length2=14, length3=28)
    df['MFI'] = ta.mfi(df['High'], df['Low'], df['Close'], df['Volume'], length=14)
    return df

def generate_signals(df, future_window=15, profit_threshold=0.1):
    df['Future_Close'] = df['Close'].shift(-future_window)
    df['Return'] = (df['Future_Close'] - df['Close']) / df['Close']
    
    # Create buy and sell conditions
    buy_condition = (df['Return'] > profit_threshold)
    sell_condition = (df['Return'] < -profit_threshold)
    
    # Create initial signals
    df['Signal'] = 0
    df.loc[buy_condition, 'Signal'] = 1
    df.loc[sell_condition, 'Signal'] = 2
    
    # Create a mask for valid signals
    valid_signal_mask = ((df['Signal'] != 0) & 
                         (df['Signal'].rolling(window=1, min_periods=1).sum().shift() == 0))
    
    # Apply the mask to keep only valid signals
    df['Signal'] = df['Signal'] * valid_signal_mask
    
    # Drop rows with NaN values
    df = df.dropna()

    # Save the transformed data to a new CSV file
    output_csv_name = f'Stock_Signals_{today}.csv'
    df.to_csv(output_csv_name, index=False)


    print(f"Transformed data saved to '{output_csv_name}'")
    return df

def fetch_trainData():

    # Clean Historical Data
    df = clean_HS()  

    # Add technical Indicators 
    df = TA_Data(df)  

    # Generate signals
    df = generate_signals(df)  

    return df

def fetch_liveData():
    # Clean Live Data
    df_ld = clean_LD() 
    
    # Clean Historical Data
    df_hs = clean_HS()  

    # Concatenate the Historical Data and Live Data
    df_ld = concat_data(df_ld, df_hs)  

    # Add technical Indicators
    df_ld = TA_Data(df_ld)  
    
    return df_ld.tail()

if __name__ == "__main__":
    # Clean Historical Data
    df = clean_HS()
    df = fetch_trainData()

    # Create subplots
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.1, subplot_titles=('Price', 'RSI'),
                        row_heights=[0.7, 0.3])

    # Add candlestick chart
    fig.add_trace(go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name='Price'),
                    row=1, col=1)

    # Add buy signals
    fig.add_trace(go.Scatter(
        x=df[df['Signal'] == 1].index,
        y=df[df['Signal'] == 1]['Close'],
        mode='markers',
        marker=dict(size=10, symbol='triangle-up', color='green'),
        name='Buy Signal'
    ), row=1, col=1)

    # Add sell signals
    fig.add_trace(go.Scatter(
        x=df[df['Signal'] == 2].index,
        y=df[df['Signal'] == 2]['Close'],
        mode='markers',
        marker=dict(size=10, symbol='triangle-down', color='red'),
        name='Sell Signal'
    ), row=1, col=1)

    # Add RSI
    fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI'),
                    row=2, col=1)

    # Add RSI overbought/oversold lines
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

    # Update layout
    fig.update_layout(
        title=f'{TICKER} Price and Signals',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False
    )

    # Show plot
    fig.show()