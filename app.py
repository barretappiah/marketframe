import streamlit as st
from data import df_maker
import plotly.express as px
import plotly.graph_objects as go

# BASIC SETTINGS
st.title("Tesla, Inc. (TSLA)")
ticker = 'TSLA'
duration = 100
interval = '1h'


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

    st.plotly_chart(fig, use_container_width=True)

def main():
    # Dataframe
    df = get_info(ticker, duration, interval)

    # Graph
    interactive_plot(df)

main()
