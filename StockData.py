import pandas as pd
import config

from datetime import date
from datetime import timedelta

from alpaca.data import  StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest

API_KEY = config.API_KEY
API_SECRETKEY = config.SECRET_KEY
TICKER = config.TICKER_SYMBOL

stock_client = StockHistoricalDataClient(API_KEY,API_SECRETKEY)

today = str(date.today())
yesterday = str(date.today() - timedelta(days = 1))


requestParams_hour = StockBarsRequest(
  symbol_or_symbols = [TICKER],
  timeframe         = TimeFrame.Hour,
  start             = yesterday,
  end               = today,
  adjustment        = 'all'
)

requestParams_minute = StockBarsRequest(
  symbol_or_symbols = [TICKER],
  timeframe         = TimeFrame.Minute,
  start             = yesterday,
  end               = today,
  adjustment        = 'all'
)
def fetchHS(choice):
    match choice:
        case "Hour":
            data = stock_client.get_stock_bars(requestParams_hour)
            df = data.df
            csvName = "HS_"+TICKER + "_" + today + "_Hour.csv"
            df.to_csv(csvName, index=False)
            print(df.head())
            print(df.tail())
            return df 
            
        case "Minute":
            data = stock_client.get_stock_bars(requestParams_minute)
            df = data.df
            csvName = "HS_"+TICKER + "_" + today + "_Minute.csv"
            df.to_csv(csvName, index=False)
            print(df.head())
            print(df.tail())
            return df
        
    
if __name__ == "__main__":
    fetchHS("Hour")  
    
  
    