import yfinance as yf
from datetime import date, datetime, timedelta

def get_data(ticker, begin, stop):
    df = yf.download(ticker, start=begin, end=stop, auto_adjust=True)
    df.dropna(inplace=True)
    df.columns = df.columns.droplevel(1)
    return df

def df_maker(ticker, duration):

    begin = date.today() - timedelta(duration)
    stop = date.today()

    df = get_data(ticker, begin, stop)
    return df

