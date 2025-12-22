import yfinance as yf
from datetime import date

def get_data(ticker, start, end):
    df = yf.download(ticker)
    df.dropna(inplace=True)
    return df

ticker = "TSLA"
start = date(2024, 1, 1)
end = date(2024, 12, 31)

print(get_data(ticker, start, end))