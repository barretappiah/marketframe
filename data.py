import pandas as pd
import yfinance as yf
from datetime import date, timedelta, timezone, datetime


# ---------------------------------------------------------------------------- #
# Get Stock Prices

def get_data(ticker, begin, stop, gap):

    # yFinance if not rate limited
    try:
        # Close Prices
        df = yf.download(ticker, start=begin, end=stop, interval=gap, auto_adjust=True)[["Close"]]
        

        # Moving Averages
        df["MA_20"] = df['Close'].rolling(20).mean()
        df["MA_50"] = df['Close'].rolling(50).mean()

        # Remove Useless Space
        df.dropna(inplace=True)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
        return df
    
    # otherwise use backup
    except Exception as e:
        print(f"⚠️ yfinance failed, loading CSV instead\n{e}")
        df = pd.read_csv(
            f"data/{ticker.lower()}_1h_1y.csv",
            parse_dates=["Date"],
            index_col="Date")
        return df

def df_maker(ticker, duration, interval):

    begin = date.today() - timedelta(duration)
    stop = date.today()

    df = get_data(ticker, begin, stop, interval)
    df.to_csv(f"data/{ticker.lower()}_1h_1y.csv")
    return df



# ---------------------------------------------------------------------------- #
# Get Company Title

def ticker_info(ticker):
    stock = yf.Ticker(ticker)

    company_name = stock.info.get("longName")
    symbol = stock.info.get("symbol")

    exchange = stock.info.get("fullExchangeName")

    return f"{company_name} ({symbol})", exchange



# ---------------------------------------------------------------------------- #
# Get Daily Change

def get_daily_change(df):
    last_close = df["Close"].iloc[-1]
    prev_clsoe = df["Close"].iloc[-2]

    raw_change = last_close - prev_clsoe
    percent_change = (raw_change / last_close) * 100

    return raw_change, percent_change



# ---------------------------------------------------------------------------- #
# Get News

def get_news(ticker, limit=5):
    
    stock = yf.Ticker(ticker)
    news = stock.news
    return news[:limit]

def extract_news_link(article: dict) -> str | None:
    content = article.get("content", {})

    if isinstance(content.get("canonicalUrl"), dict):
        return content["canonicalUrl"].get("url")

    if article.get("link"):
        return article["link"]

    if isinstance(content.get("clickThroughUrl"), dict):
        return content["clickThroughUrl"].get("url")

    return None

def upload_date(article):
    uploaded = article["content"]["pubDate"]
    dt = datetime.fromisoformat(uploaded.replace("Z", "+00:00"))

    now = datetime.now(timezone.utc)
    delta = now - dt

    delta_seconds = delta.total_seconds()
    seconds = int(delta_seconds)

    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24

    if days > 0:
        return f"{days}d"
    elif hours > 0:
        return f"{hours}h"
    elif minutes > 0:
        return f"{minutes}m"
    else:
        return f"{seconds}s"