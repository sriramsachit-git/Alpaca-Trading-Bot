from lumibot.backtesting import Backtest
from lumibot.strategies import Strategy
from lumibot.traders import SimulatedTrader

class SignalStrategy(Strategy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signals = None  # This will hold our signals DataFrame

    def on_data(self, data):
        current_time = data.index[-1]
        signal = self.signals.loc[current_time, 'Signal']
        
        if signal == 1:
            self.buy(symbol='AAPL', quantity=10)
        elif signal == -1:
            self.sell(symbol='AAPL', quantity=10)

if __name__ == "__main__":
    # Load your signals data
    signals_df = pd.read_csv("path_to_your_csv.csv", index_col=0, parse_dates=True)

    # Create the strategy
    strategy = SignalStrategy(trader=SimulatedTrader(), signals=signals_df)

    # Set up the backtest
    backtest = Backtest(strategy)
    backtest.run()
    backtest.results()
