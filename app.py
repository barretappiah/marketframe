import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

import data
import styles
import backtest_hold
import backtest_ma
import backtest_rsi
import backtest_blend

# ---------------------------------------------------------------------------- #

# BASIC SETTINGS
default_ticker = 'ETH-USD'
duration = 2000
interval = '1d'

# STREAMLIT SETTINGS
st.set_page_config(layout="wide")
styles.apply_styles()

dash_col, news_col = st.columns([3, 1])

st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)

# BUILD DATA-FRAME
def get_info(ticker, duration, interval):
    df = data.df_maker(ticker, duration, interval)
    return df

# SIDEBAR
stocks = ["NKE", "TSLA", "META", "PYPL", "ZM"]

for stock in stocks:
    if st.sidebar.button(stock, use_container_width=True):
        st.session_state.ticker = stock

# PLOT GRAPH
def interactive_plot(df, ma, rsi, blend):
    fig = go.Figure()

    # Close Price
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Close'],
        mode='lines',
        name='Close'
    ))

        # MA
    fig.add_trace(go.Scatter(
        x=df.index,
        y=ma,
        mode='lines',
        name='MA',
        line=dict(
            color="#00F508",
            width=2
        )
    ))

            # RSI
    fig.add_trace(go.Scatter(
        x=df.index,
        y=rsi,
        mode='lines',
        name='RSI',
        line=dict(
            color="#F50000",
            width=2
        )
    ))

                # BLEND
    fig.add_trace(go.Scatter(
        x=df.index,
        y=blend,
        mode='lines',
        name='BLEND',
        line=dict(
            color="#E5F500",
            width=2
        )
    ))

    fig.update_layout(
        legend_title = "Indicators"
    )

    fig.update_layout(margin=dict(l=10, r=10, t=25, b=10))


    dash_col.plotly_chart(fig, width='stretch')

# - Strategies --------------------------------------------------------------- #

def s_hold(df):
    backtest_hold.run_backtest(df)

def s_moving_averages(df):
    strategy = backtest_ma.run_backtest(df)
    return strategy

def s_rsi(df):
    strategy = backtest_rsi.run_backtest(df)
    return strategy

def s_blend(df):
    strategy = backtest_blend.run_backtest(df)
    return strategy

# - News --------------------------------------------------------------------- #

def news_builder(current_ticker):
    news = data.get_news(current_ticker)

    count = 1
    for article in news:
        
        title = article["content"]["title"]
        publisher = article["content"]["provider"]["displayName"]
        
        link = data.extract_news_link(article)
        upload_time = data.upload_date(article)

        news_col.markdown(
            f"""
            <span id="news-top-margin"></span>
            """, unsafe_allow_html=True
        )

        news_col.markdown(
            f"""
            <div class="news_article">
                <a href="{link}" class="news_article_link">
                    <strong class="news_title">{title}</strong>
                </a><br>
                <span class="news_article_publisher">{publisher} - {upload_time}</span>
            </div>
            """, unsafe_allow_html=True
        )

        if count < len(news):
            news_col.markdown(f"""<hr class="news_break">""", unsafe_allow_html=True)
        
        count += 1

# ---------------------------------------------------------------------------- #

def main():
    # Get ticker from session_state, else use default
    current_ticker = st.session_state.get('ticker', default_ticker)
    
    # Dataframe
    df = get_info(current_ticker, duration, interval)

    # Title
    stock_title, exchange = data.ticker_info(current_ticker)
    raw_change, percent_change = data.get_daily_change(df)

    dash_col.markdown(f'<div id="exchange-caption">{exchange}</div>', unsafe_allow_html=True)
    dash_col.markdown(f'<h1 class="stock-title">{stock_title}</h1>', unsafe_allow_html=True)
    dash_col.markdown(styles.percent_badge(percent_change), unsafe_allow_html=True)

    # News
    news_builder(current_ticker)

    # Graph
    strat_hold = s_hold(df)
    strat_ma = s_moving_averages(df)
    strat_rsi = s_rsi(df)
    strat_blend = s_blend(df)

    interactive_plot(df, strat_ma, strat_rsi, strat_blend)

main()