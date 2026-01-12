

def rate_of_change(df):
    close_next = df['Close'].iloc[-1]
    close_now = df['Close'].iloc[0]

    change = 1 + ((close_next - close_now) / close_now)
    return change

def execute_change(change, holdings):
    holdings *= change
    return holdings


def run_backtest(df):

    holdings = 10000

    change = rate_of_change(df)
    holdings = execute_change(change, holdings)
   
    portfolio = holdings
    print(f'HOLD: {portfolio}')