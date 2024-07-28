import pandas as pd
import config
import os 

from datetime import date,datetime,timedelta


from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest

from alpaca.data import  StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest

API_KEY = config.API_KEY
API_SECRETKEY = config.SECRET_KEY

client = CryptoHistoricalDataClient()
stock_client = StockHistoricalDataClient(API_KEY,API_SECRETKEY)


def fetchHS(Timeframe,start,end,TICKER):
    
    match Timeframe:
      case "Hour":
          time_frame = TimeFrame.Hour
           
      case "Minute":
          time_frame = TimeFrame.Minute

    start_time = datetime.strptime(start, '%m-%d-%Y').date()
    end_time = datetime.strptime(end, '%m-%d-%Y').date()

    requestParams = StockBarsRequest(
        symbol_or_symbols = [TICKER],
        timeframe         = TimeFrame.time_frame,
        start             = start,
        end               = end,
        adjustment        = 'all'
        )

    data = stock_client.get_stock_bars(requestParams)
    df = data.df

    df.reset_index(inplace=True)
    #df = df.drop(['symbol'], axis=1)

    csvName =  "HS_"+TICKER+ ".CSV"
    df.to_csv(csvName, index=False)

    print(df.head())
    print(df.tail())
    return df 
            
        
        
def fetchCrypto(Timeframe,start,end,TICKER):
    match Timeframe:
        case "Hour":
          time_frame = TimeFrame.Hour
           
        case "Minute":
          time_frame = TimeFrame.Minute

    start_time = datetime.strptime(start, '%m-%d-%Y').date()
    #end_time  = datetime.strptime(end, '%m-%d-%Y').date()
    
    request_params = CryptoBarsRequest(
                              symbol_or_symbols = TICKER,
                              timeframe = time_frame,
                              start = start_time,
                              end = end
                      )

    bars = client.get_crypto_bars(request_params)
        
    df = bars.df

    df.reset_index(inplace=True)
    #df = df.drop(['symbol'], axis=1) 

    csvName = "HS_"+"BTC"+".CSV"
    df.to_csv(csvName, index=False)

    return df 
        
        
    
if __name__ == "__main__":

  yesterday = str(date.today() - timedelta(days = 1))
  #%m-%d-%Y
  df = fetchCrypto("Hour","1-12-2023",yesterday)
  
  print(df.head())
  print(df.tail())

  
  #df = fetchHS("Hour")
  #print(df.head())
  #print(df.tail())
    
