import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

signals_data = pd.read_csv('Stock_Signals.csv')
# Function to backtest the strategy with buy and sell signals
def backtest_with_sell(df, initial_capital, take_profit, stop_loss):
    capital = initial_capital
    positions = []
    returns = []
    trade_durations = []
    trade_count = 0
    max_profit = 0
    for i in range(1, len(df)):
        if df['Signal'][i] == 1:  # Buy signal
            entry_price = df['Close'][i]
            tp_price = entry_price * (1 + take_profit)
            sl_price = entry_price * (1 - stop_loss)
            for j in range(i+1, len(df)):
                high = df['Close'][j]
                low = df['Close'][j]
                duration = j - i
                if high >= tp_price:
                    capital += capital * take_profit
                    returns.append(take_profit)
                    positions.append((entry_price, tp_price, 'Take Profit', 'Buy', duration))
                    trade_durations.append(duration)
                    trade_count += 1
                    max_profit = max(max_profit, take_profit)
                    break
                elif low <= sl_price:
                    capital -= capital * stop_loss
                    returns.append(-stop_loss)
                    positions.append((entry_price, sl_price, 'Stop Loss', 'Buy', duration))
                    trade_durations.append(duration)
                    trade_count += 1
                    break
        elif df['Signal'][i] == -1:  # Sell signal
            entry_price = df['Close'][i]
            tp_price = entry_price * (1 - take_profit)
            sl_price = entry_price * (1 + stop_loss)
            for j in range(i+1, len(df)):
                high = df['Close'][j]
                low = df['Close'][j]
                duration = j - i
                if low <= tp_price:
                    capital += capital * take_profit
                    returns.append(take_profit)
                    positions.append((entry_price, tp_price, 'Take Profit', 'Sell', duration))
                    trade_durations.append(duration)
                    trade_count += 1
                    max_profit = max(max_profit, take_profit)
                    break
                elif high >= sl_price:
                    capital -= capital * stop_loss
                    returns.append(-stop_loss)
                    positions.append((entry_price, sl_price, 'Stop Loss', 'Sell', duration))
                    trade_durations.append(duration)
                    trade_count += 1
                    break

    avg_return = sum(returns) / trade_count if trade_count > 0 else 0
    avg_duration = sum(trade_durations) / trade_count if trade_count > 0 else 0
    return capital, avg_return, avg_duration, max_profit, trade_count, positions, returns

# Load your data
# Ensure your DataFrame has columns: 'Close', 'Signal'
# Example: signals_data = pd.read_csv('your_file.csv')

initial_capital = 1000
take_profit = 0.03  # 3%
stop_loss = 0.01    # 1%

# Backtesting the strategy with both buy and sell signals
final_capital, avg_return, avg_duration, max_profit, total_trades, trade_details, returns = backtest_with_sell(signals_data, initial_capital, take_profit, stop_loss)

# Calculate monthly and yearly returns
signals_data['Date'] = pd.to_datetime(signals_data.index, unit='s')
signals_data.set_index('Date', inplace=True)
monthly_returns = signals_data['Close'].resample('M').ffill().pct_change().mean()
yearly_returns = signals_data['Close'].resample('Y').ffill().pct_change().mean()

# Calculate buy and hold returns
initial_price = signals_data['Close'].iloc[0]
final_price = signals_data['Close'].iloc[-1]
buy_and_hold_return = (final_price - initial_price) / initial_price

# Plotting cumulative returns and buy-and-hold comparison
cumulative_returns = np.cumsum(returns) * initial_capital
buy_and_hold_cumulative = (signals_data['Close'] / initial_price - 1) * initial_capital

plt.figure(figsize=(14, 7))
plt.plot(cumulative_returns, label='Strategy Cumulative Returns')
plt.plot(buy_and_hold_cumulative.values, label='Buy and Hold Cumulative Returns', linestyle='--')
plt.xlabel('Trade Number')
plt.ylabel('Cumulative Return')
plt.title('Cumulative Returns: Strategy vs Buy and Hold')
plt.legend()
plt.grid(True)
plt.show()

# Display the final statistics
print(f"Final Capital: ${final_capital:.2f}")
print(f"Average Return per Trade: {avg_return:.2%}")
print(f"Average Trade Duration: {avg_duration} periods")
print(f"Maximum Profit per Trade: {max_profit:.2%}")
print(f"Total Trades: {total_trades}")
print(f"Monthly Average Return: {monthly_returns:.2%}")
print(f"Yearly Average Return: {yearly_returns:.2%}")
print(f"Buy and Hold Return: {buy_and_hold_return:.2%}")
