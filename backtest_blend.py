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


def get_price_data(df):
    prices = []

    for i in range(len(df)):
        close = float(df["Close"].iloc[i])
        ma20 = df["MA_20"].iloc[i]
        ma50 = df["MA_50"].iloc[i]
        rsi = df["RSI"].iloc[i]

        prices.append([close, ma20, ma50, rsi])

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
    df = df.copy()
    df = calculate_rsi(df, period)

    strategy = []
    prices = get_price_data(df)

    days = len(df)
    trades = 0

    cash = float(df["Close"].iloc[0])
    start = cash
    holdings = 0

    for i in range(days - 1):
        close, ma20, ma50, rsi = prices[i]

        # Skip days where indicators are not ready yet
        if pd.isna(ma20) or pd.isna(ma50) or pd.isna(rsi):
            portfolio = holdings + cash
            strategy.append(portfolio)
            continue

        # Individual signals
        ma_buy_signal = close > ma20 > ma50
        ma_sell_signal = not ma_buy_signal

        rsi_buy_signal = rsi < rsi_buy
        rsi_sell_signal = rsi > rsi_sell


        if ma_buy_signal:
            ma_since = 0


        # Blended logic:
        # Buy only if any says buy
        if ma_buy_signal or rsi_buy_signal:
            old_cash, old_holdings = cash, holdings
            cash, holdings = buy_stock(cash, holdings)
            if (old_cash, old_holdings) != (cash, holdings):
                trades += 1

        # Sell if no strat wants to buy/hold
        else:
            cash, holdings = sell_stock(cash, holdings)
            if (old_cash, old_holdings) != (cash, holdings):
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