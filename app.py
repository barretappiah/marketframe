import streamlit as st
from data import df_maker
import plotly.express as px

st.title("Title")

df = (df_maker('TSLA', 30))

def interactive_plot(df):
    if df is None or df.empty:
        raise ValueError('No Data')
    plot = px.line(df, x=df.index, y='Close', line_shape='linear')
    st.plotly_chart(plot)

interactive_plot(df)
