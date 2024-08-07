# data_collection.py
import yfinance as yf
import pandas as pd

def get_historical_data(stock_symbol, start_date, end_date):
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    stock_data = stock_data[['Close']]
    return stock_data

if __name__ == "__main__":
    data = get_historical_data("RELIANCE.BO", "2010-01-01", "2023-01-01")
    print(data.head())
