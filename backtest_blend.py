import pandas as pd

def calculate_rsi(df, period=14):
    delta = df["Close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    return df


def get_close_and_rsi(df):
    prices = []

    for i in range(len(df)):
        close = float(df["Close"].iloc[i])
        rsi = df["RSI"].iloc[i]
        prices.append([close, rsi])

    return prices


def buy_stock(cash, holdings):
    if cash == 0:
        return cash, holdings

    holdings = cash
    cash = 0
    return cash, holdings


def sell_stock(cash, holdings):
    if holdings == 0:
        return cash, holdings

    cash = holdings
    holdings = 0
    return cash, holdings


def rate_of_change(df, i):
    close_next = df["Close"].iloc[i + 1]
    close_now = df["Close"].iloc[i]

    change = 1 + ((close_next - close_now) / close_now)
    return change


def execute_change(change, holdings):
    holdings *= change
    return holdings


def run_backtest(df, rsi_buy=30, rsi_sell=70, period=14):
    df = calculate_rsi(df, period)
    strategy = []
    prices = get_close_and_rsi(df)

    days = len(df)
    trades = 0

    cash = float(df["Close"].iloc[0])
    start = cash
    holdings = 0

    for i in range(days - 1):
        close, rsi = prices[i]

        # Skip days where RSI is NaN at the beginning
        if pd.isna(rsi):
            portfolio = holdings + cash
            strategy.append(portfolio)
            continue

        if rsi < rsi_buy:
            cash, holdings = buy_stock(cash, holdings)
            trades += 1
        elif rsi > rsi_sell:
            cash, holdings = sell_stock(cash, holdings)
            trades += 1

        if holdings > 0:
            change = rate_of_change(df, i)
            holdings = execute_change(change, holdings)

        portfolio = holdings + cash
        strategy.append(portfolio)

    portfolio = holdings + cash
    print(f"DAYS: {days - 1}")
    print(f"START: {start}")
    print(f"END: {portfolio}")
    print(f"TRADES: {trades}")
    return strategy