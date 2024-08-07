import pandas as pd
import pandas_ta as ta
from datetime import date
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Constants
today = str(date.today())

def clean_LD(df):
    # Adding timestamp
    if 't' in df.columns:
        df = df.rename(columns={'t': 'timestamp', 'o': 'Open', 'h': 'High', 'l': 'Low', 'c': 'Close', 'v': 'Volume', 'S': 'symbol'})
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
    return df

def clean_HS(df):
    grouped_dfs = {}
    
    # Group by the 'symbol' column
    grouped = df.groupby('symbol')
    
    for symbol, group in grouped:
        # Adding timestamp if necessary
        if 'timestamp' in group.columns:
            group['timestamp'] = pd.to_datetime(group['timestamp'])
            group.set_index('timestamp', inplace=True)
        
        # Rename the required Columns
        group = group.rename(columns={'open': 'Open', 'low': 'Low', 'close': 'Close', 'high': 'High', 'volume': 'Volume'})
        
        grouped_dfs[symbol] = group
    
    return grouped_dfs

def concat_data(df_ld, df_hs): # Some Technical Indicators need more values to be calculated
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

def generate_signals(df, future_window=10, profit_threshold=0.05):
    df['Future_Close'] = df['Close'].shift(-future_window)
    df['Return'] = (df['Future_Close'] - df['Close']) / df['Close']
    
    # Create buy and sell conditions
    buy_condition = (df['Return'] > profit_threshold)
    sell_condition = (df['Return'] < -profit_threshold)
    
    # Create initial signals
    df['Signal'] = 0
    df.loc[buy_condition, 'Signal'] = 1
    df.loc[sell_condition, 'Signal'] = 2

    # Save the transformed data to a new CSV file
    output_csv_name = f'Stock_Signals_{df["symbol"].iloc[0]}.csv'
    df.to_csv(output_csv_name, index=False)
    print(f"Transformed data saved to '{output_csv_name}'")
    return df

def fetch_trainData(df_hs):
    # Clean Historical Data
    grouped_dfs = clean_HS(df_hs)
    
    # Process each stock separately
    processed_dfs = {}
    for symbol, df in grouped_dfs.items():
        # Add technical Indicators 
        df = TA_Data(df)
        
        # Generate signals
        df = generate_signals(df)
        
        processed_dfs[symbol] = df

    return processed_dfs

def fetch_liveData(df_hs):
    df_ld = pd.read_csv("LiveData.csv")
    
    # Clean Live Data
    df_ld = clean_LD(df_ld) 
    
    # Clean Historical Data
    df_hs = clean_HS(df_hs)
    
    live_data = {}
    for symbol, df_hs_group in df_hs.items():
        df_hs_group = df_hs_group.tail(20)  

        # Filter live data for the current symbol
        df_ld_group = df_ld[df_ld['symbol'] == symbol]

        # Concatenate the Historical Data and Live Data
        df = concat_data(df_ld_group, df_hs_group)  

        # Add technical Indicators
        df = TA_Data(df)
        
        live_data[symbol] = df.tail()

    return live_data

if __name__ == "__main__":
    # Load data from uploaded files
    df_hs = pd.read_csv("HS.CSV")
    
    # Fetch and process training data for each stock
    processed_dfs = fetch_trainData(df_hs)
    
    for symbol, df in processed_dfs.items():
        # Count the number of buy and sell signals for each stock
        num_buy_signals = df[df['Signal'] == 1].shape[0]
        num_sell_signals = df[df['Signal'] == 2].shape[0]

        print(f"Stock: {symbol}")
        print(f"Number of Buy Signals: {num_buy_signals}")
        print(f"Number of Sell Signals: {num_sell_signals}")
        
        # Plotting for each stock
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
            title=f'{symbol} Price and Signals',
            yaxis_title='Price',
            xaxis_rangeslider_visible=False
        )

        # Show plot
        fig.show()
