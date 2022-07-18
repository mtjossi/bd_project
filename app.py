import streamlit as st
import pandas as pd
import quantstats as qs
import mplfinance as mpf
import data_list
from ta import add_all_ta_features
from ta.utils import dropna
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit.components.v1 import html
import numpy as np
st.set_option('deprecation.showPyplotGlobalUse', False)
from tradingview_ta import TA_Handler, Interval, Exchange
from PIL import Image


st.title('Crypto Dashboard')
st.write("More pages on the left / sidebar")

c1, c2, c3 = st.columns([1,1,1])
crypto_list1 = dict(zip(data_list.crypto_list['name'], data_list.crypto_list['ticker']))

with c1:
    c_choice = st.selectbox("Main Crypto to Plot", crypto_list1.keys())
    df = pd.read_parquet(f'./data/Alpaca/{crypto_list1[c_choice]}USD.parquet')
with c2:
    st.write('')
with c3:
    st.markdown('&nbsp;')
    show_data = st.checkbox('Show data table', False)

st.markdown('---')
fred_dict = dict(zip(data_list.fred_list['fred_names'], data_list.fred_list['fred_tickers']))


# st.dataframe(df)
coin_sell = TA_Handler(
    symbol=f"{crypto_list1[c_choice]}USD",
    screener="crypto",
    exchange="COINBASE",
    interval=Interval.INTERVAL_1_DAY
)
ana = coin_sell.get_analysis().summary
buy_percent = np.floor((ana['BUY'] / (ana['BUY'] + ana['SELL'] + ana['NEUTRAL']))*100)
st.success(f"Recommendation: {ana['RECOMMENDATION']}")
st.success(f"{buy_percent}% recommendation to buy")

main_fig = mpf.plot(df, type='line')
st.pyplot(main_fig)

st.dataframe(df.describe())

st.warning("Please use the get_ts.ipynb in the notebook folder to get the tear sheets")

if show_data:
    st.markdown('---')
    st.dataframe(df)
