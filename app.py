import streamlit as st
from data import df_maker
from data import ticker_info
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------------------------- #

# BASIC SETTINGS
default_ticker = 'NVDA'
duration = 365
interval = '1d'


# BUILD DATA-FRAME
def get_info(ticker, duration, interval):
    df = df_maker(ticker, duration, interval)
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

    st.plotly_chart(fig, width='stretch')

# ---------------------------------------------------------------------------- #

def main():
    # Get ticker from session_state, else use default
    current_ticker = st.session_state.get('ticker', default_ticker)
    
    # Dataframe
    df = get_info(current_ticker, duration, interval)

    # Title
    st.title(ticker_info(current_ticker))

    # Graph
    interactive_plot(df)

main()

