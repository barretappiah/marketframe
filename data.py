import pandas as pd
import yfinance as yf
from datetime import date, timedelta

# ---------------------------------------------------------------------------- #

def get_data(ticker, begin, stop, gap):
    # Close Prices
    df = yf.download(ticker, start=begin, end=stop, interval=gap, auto_adjust=True)

    # Moving Averages
    df["MA_20"] = df['Close'].rolling(20).mean()
    df["MA_50"] = df['Close'].rolling(50).mean()

    # Remove Useless Space
    df.dropna(inplace=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    return df

def df_maker(ticker, duration, interval):

    begin = date.today() - timedelta(duration)
    stop = date.today()

    df = get_data(ticker, begin, stop, interval)
    return df


# ---------------------------------------------------------------------------- #

def ticker_info(ticker):
    stock = yf.Ticker(ticker)

    company_name = stock.info.get("longName")
    symbol = stock.info.get("symbol")

    return f"{company_name} ({symbol})"