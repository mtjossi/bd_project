import  streamlit as st
import ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.title('TA Strategies')

import pandas as pd 
import numpy as np
import sqlite3
import ta

conn = sqlite3.connect('./test.db')

df = pd.read_sql(sql="select date, open, high, low, close, volume from crypto_prices where ticker = 'BTCUSD'", con=conn)

df.columns = ['date', 'open', 'high', 'low', 'close', 'volume', ]
# df['date'] = df['date'].apply(lambda x: x.date())

WINDOW = st.slider("Enter a window: ", 1, 300, 30)
df['bb_h'] = ta.volatility.BollingerBands(close=df['close'], window=WINDOW, fillna=True).bollinger_hband()
df['bb_m'] = ta.volatility.BollingerBands(close=df['close'], window=WINDOW, fillna=True).bollinger_mavg()
df['bb_l'] = ta.volatility.BollingerBands(close=df['close'], window=WINDOW, fillna=True).bollinger_lband()


fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_traces(go.Candlestick(x=df['date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'], name='candlestick'))
fig.add_traces(go.Bar(x=df['date'], y=df['volume'], name='volume'))
fig.add_traces(go.Scatter(x=df['date'], y=df['bb_h'], name='bb_high',
                          line = {'dash': 'dash'},))
fig.add_traces(go.Scatter(x=df['date'], y=df['bb_l'], name='bb_low',
                          line = {'dash': 'dash'},
                         fill = 'tonexty',
                         opacity = 0.5))
fig.update_layout(height=500, width=1000, title_text="Bollinger Bands", xaxis_rangeslider_visible=True)
st.plotly_chart(fig)
st.write("Sample strategy: Buy when price leaves, then re-enters Lower Bollinger Band")
st.write("Sample strategy: Sell when price leaves, then re-enters Upper Bollinger Band")


st.sidebar.write("Parameters for TAs")
W1 = st.sidebar.slider("short window", 1,10,3)
W2 = st.sidebar.slider("long window", 1,100,37)
W = 10
POW1 = st.sidebar.slider("power 1", 1,20,2)
POW2 = st.sidebar.slider("power 2", 1,100,30)

df['ao'] = ta.momentum.AwesomeOscillatorIndicator(high=df['high'], low=df['low'], window1=W1, window2=W2, fillna=True).awesome_oscillator()
df['kama'] = ta.momentum.KAMAIndicator(close=df['close'], window=W, pow1=POW1, pow2=POW2, fillna=True).kama()
df['roc'] = ta.momentum.ROCIndicator(close=df['close'], window=W, fillna=True).roc()
df['rsi'] = ta.momentum.RSIIndicator(close=df['close'], window=W, fillna=True).rsi()


fig2 = make_subplots(rows=6, cols=1)
fig2.append_trace(go.Candlestick(x=df['date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'], name='candlestick'), row=1, col=1)
fig2.append_trace(go.Bar(x=df['date'], y=df['volume'], name='volume'), row=1, col=1)


fig2.append_trace(go.Scatter(x=df['date'], y=df['ao']/np.max(df['ao']), name='ao'), row=3, col=1)
fig2.append_trace(go.Scatter(x=df['date'], y=df['kama']/np.max(df['kama']), name='kama',
                         opacity = 0.5), row=4, col=1)
fig2.append_trace(go.Scatter(x=df['date'], y=df['rsi']/np.max(df['rsi']), name='rsi'), row=5, col=1)
fig2.append_trace(go.Scatter(x=df['date'], y=df['roc']/np.max(df['roc']), name='roc', opacity = 0.5), row=6, col=1)
fig2.update_layout(height=1000, width=1000, title_text="Stacked TAs", xaxis_rangeslider_visible=True)
fig2.update_xaxes(matches='x')
st.plotly_chart(fig2)



st.write("""
- An increase in the fed fund rate results in a decrease in BTC price.
- If the change in fed fund rate can be predicted (using other macro variables such as GDP, 10-year bond yields, non-farm payrolls, etc.), maybe the change in BTC prices can also be predicted.
- These are all data we have gotten from FRED, so sourcing the data is not a problem.
""")
