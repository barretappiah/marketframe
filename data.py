import yfinance as yf
from datetime import date, datetime, timedelta

def get_data(ticker, begin, stop, gap):
    df = yf.download(ticker, start=begin, end=stop, interval=gap, auto_adjust=True)
    df.dropna(inplace=True)
    df.columns = df.columns.droplevel(1)
    return df

def df_maker(ticker, duration, interval):

    begin = date.today() - timedelta(duration)
    stop = date.today()

    df = get_data(ticker, begin, stop, interval)
    return df