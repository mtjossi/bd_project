import streamlit as st
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
import matplotlib.pyplot as plt
import numpy as np
st.set_option('deprecation.showPyplotGlobalUse', False)


st.title('Crypto Dashboard')

c1, c2, c3 = st.columns([1,1,1])
crypto_list1 = dict(zip(data_list.crypto_list['name'], data_list.crypto_list['ticker']))

with c1:
    c_choice = st.selectbox("Main Crypto to Plot", crypto_list1.keys())
    df = pd.read_parquet(f'./data/Alpaca/{crypto_list1[c_choice]}USD.parquet')
with c2:
    st.write('   ')
with c3:
    st.markdown('&nbsp;')
    show_data = st.checkbox('Show data table', False)

st.markdown('---')
fred_dict = dict(zip(data_list.fred_list['fred_names'], data_list.fred_list['fred_tickers']))
fred_selection = st.sidebar.multiselect("Plot as well:", data_list.fred_list['fred_names'])
# st.write(fred_selection)

st.dataframe(df)
main_fig = mpf.plot(df, type='line')
st.pyplot(main_fig)

fig, axs = plt.subplots(len(fred_selection), 1, figsize=(15,15))


for i in range(len(fred_selection)):
    temp = pd.read_parquet(f'./data/FRED/{fred_dict[fred_selection[i]]}.parquet')
    st.write(df.index[0].date())
    st.write(np.min(df.index).date())
    temp = temp[pd.to_datetime(temp.index)>=pd.to_datetime(np.min(df.index))]
    # st.dataframe(temp)
    axs[i].plot(temp.index, temp.iloc[:,0])
    axs[i].set_title(fred_selection[i])
    axs[i].grid(True)

fig.tight_layout()
st.pyplot(fig)



if show_data:
    st.markdown('---')
    st.dataframe(df)