def get_close(df):
    prices = []

    for i in range(len(df)):
        close = df["Close"].iloc[i]
        ma20 = df["MA_20"].iloc[i]
        ma50 = df["MA_50"].iloc[i]
        
        prices.append([float(close), float(ma20), float(ma50)])
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
    close_next = df['Close'].iloc[i + 1]
    close_now = df['Close'].iloc[i]

    change = 1 + ((close_next - close_now) / close_now)
    return change

def execute_change(change, holdings):
    holdings *= change
    return holdings


def run_backtest(df):
    strategy = []
    prices = get_close(df)

    days = len(df)
    trades = 0

    cash = df['Close'].iloc[0]
    start = cash
    holdings = 0

    for i in range(days - 1):
        close, ma20, ma50 = prices[i]
        in_position = (close > ma20 > ma50)

        if in_position:
            cash, holdings = buy_stock(cash, holdings)
        else:
            cash, holdings = sell_stock(cash, holdings)
        trades += 1

        if holdings > 0:
            change = rate_of_change(df, i)
            holdings *= change
        

        portfolio = holdings + cash
        strategy.append(portfolio)
        
    portfolio = holdings + cash
    print(f'DAYS: {trades}')
    print(f'START: {start}')
    print(f'TRADE: {portfolio}')
    return strategy
    