import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

import data
import styles
import backtest
import backtest_hold

# ---------------------------------------------------------------------------- #

# BASIC SETTINGS
default_ticker = 'NVDA'
duration = 365
interval = '1d'

# STREAMLIT SETTINGS
st.set_page_config(layout="wide")
styles.apply_styles()

dash_col, news_col = st.columns([3, 1])

# BUILD DATA-FRAME
def get_info(ticker, duration, interval):
    df = data.df_maker(ticker, duration, interval)
    return df


# PLOT GRAPH
def interactive_plot(df):
    fig = go.Figure()

    # Close Price
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Close'],
        mode='lines',
        name='Close'
    ))

    # MA 20
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['MA_20'],
        mode='lines',
        name='MA 20'
    ))

        # MA 50
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['MA_50'],
        mode='lines',
        name='MA 50'
    ))

    fig.update_layout(
        legend_title = "Indicators"
    )

    fig.update_layout(margin=dict(l=10, r=10, t=25, b=10))


    dash_col.plotly_chart(fig, width='stretch')

# ---------------------------------------------------------------------------- #

def trade(df):
    backtest.run_backtest(df)

def hold(df):
    backtest_hold.run_backtest(df)

# ---------------------------------------------------------------------------- #

def main():
    # Get ticker from session_state, else use default
    current_ticker = st.session_state.get('ticker', default_ticker)
    
    # Dataframe
    df = get_info(current_ticker, duration, interval)

    # Title
    stock_title, exchange = data.ticker_info(current_ticker)
    raw_change, percent_change = data.get_daily_change(df)

    dash_col.markdown('<div id="exchange-caption">NasdaqGS</div>', unsafe_allow_html=True)
    dash_col.markdown(f'<h1 class="stock-title">{stock_title}</h1>', unsafe_allow_html=True)
    dash_col.markdown(styles.percent_badge(percent_change), unsafe_allow_html=True)

    # News
    news = data.get_news(current_ticker)

    for article in news:
        title = article["content"]["title"]
        publisher = article.get("publisher")

        link = data.extract_news_link(article)

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
                <span class="news_article_publisher">{publisher}</span>
            </div>
            <hr class="news_break">
            """, unsafe_allow_html=True
        )


    # Graph
    interactive_plot(df)

    trade(df)
    hold(df)

main()

