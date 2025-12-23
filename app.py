import streamlit as st
from data import df_maker
import plotly.express as px

# BASIC SETTINGS
st.title("Tesla, Inc. (TSLA)")
ticker = 'TSLA'
duration = 20
interval = '1h'

# BUILD DATA-FRAME
def get_info(ticker, duration, interval):
    df = df_maker(ticker, duration, interval)
    return df

# PLOT GRAPH
def interactive_plot(df):
    plot = px.line(df, x=df.index, y='Close', line_shape='linear')
    st.plotly_chart(plot)


def main():
    # Dataframe
    df = get_info(ticker, duration, interval)

    # Graph
    interactive_plot(df)

main()
