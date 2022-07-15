import  streamlit as st

st.title('Indicators')

import pandas as pd
import requests
import yfinance as yf
import pandas_datareader.data as pdr
from alpaca_trade_api.rest import REST
import quantstats as qs
import mplfinance as mpf
import data_list
from ta import add_all_ta_features
from ta.utils import dropna
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit.components.v1 import html
import sqlite3
conn = sqlite3.connect('./test.db')


c1, c2, c3 = st.columns([1,1,1])
crypto_list1 = dict(zip(data_list.crypto_list['name'], data_list.crypto_list['ticker']))

with c1:
    c_choice = st.selectbox("Main Crypto to Plot", crypto_list1.keys())
    # df = pd.read_parquet(f'./data/Alpaca/{crypto_list1[c_choice]}USD.parquet')
    df = pd.read_sql(sql=f"select * from crypto_prices where ticker = '{crypto_list1[c_choice]}USD'", con=conn)
with c2:
    st.write(' ')
with c3:
    st.markdown('&nbsp;')
    show_data = st.checkbox('Show data table', False)

st.markdown('---')

st.sidebar.subheader('Settings & SMA')
st.sidebar.caption('Adjust charts settings and then press apply')

with st.sidebar.form('settings_form'):
    show_nontrading_days = st.checkbox('Show non-trading days', True)
    chart_styles = [
        'default', 'binance', 'checkers', 'classic', 'sas'
    ]
    chart_style = st.selectbox('Chart style', options=chart_styles, index=chart_styles.index('default'))
    chart_types = [
        'candle', 'ohlc', 'line', 'renko', 'pnf'
    ]
    chart_type = st.selectbox('Chart type', options=chart_types, index=chart_types.index('candle'))

    mav1 = st.slider('SMA 1', min_value=3, max_value=30, value=5, step=1)
    mav2 = st.slider('SMA 2', min_value=3, max_value=30, value=30, step=1)
    mav3 = st.slider('SMA 3', min_value=3, max_value=200, value=120, step=1)

    st.form_submit_button('Apply')
df['date'] = pd.to_datetime(df['date'])
df2 = df.set_index('date')

fig, ax = mpf.plot(
    df2,
    title=f'{crypto_list1[c_choice]}',
    type=chart_type,
    show_nontrading=show_nontrading_days,
    mav=(int(mav1),int(mav2),int(mav3)),
    volume=True,

    style=chart_style,
    figsize=(15,10),

    returnfig=True
)

st.pyplot(fig)

if show_data:
    st.markdown('---')
    df['date'] = df['date'].apply(lambda x: x.date())
    st.dataframe(df)




