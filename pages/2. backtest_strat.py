import  streamlit as st
import ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

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



st.write("- - - -")
fig22 = plt.figure()
btc2 = pd.read_sql(sql="select date, close from crypto_prices where ticker='BTCUSD'", con=conn)
btc2.columns = ['date', 'BTC']
btc2['date'] = pd.to_datetime(btc2['date'])
btc2 = btc2.set_index('date')

plt.plot(btc2.index, btc2['BTC']/max(btc2['BTC']), label='BTC scaled price')
daily_stuff = ["DFII10", "T10YIE"]
for d in daily_stuff:
    temp = pd.read_parquet(f'./data/FRED/{d}.parquet')
    plt.plot(temp.index, temp[d], label=d)
    
plt.legend(loc=0)
st.pyplot(fig22)



st.write("- - - -")
st.subheader("BTC correlation")

btc = pd.read_sql(sql="select date, close from crypto_prices where ticker='BTCUSD'", con=conn)
btc.columns = ['date', 'BTC']
btc['date'] = pd.to_datetime(btc['date'])
btc = btc.set_index('date')
btc = btc.pct_change().resample('M').agg(lambda x: (x+1).prod() - 1)
btc.index = btc.index - pd.offsets.BMonthBegin(1)

macro_list = ["UNRATE", "FEDFUNDS", "PAYEMS", "CPIAUCSL"]
comb_df = pd.DataFrame()
for m in macro_list:
    temp = pd.read_parquet(f'./data/FRED/{m}.parquet')
    comb_df = pd.concat([comb_df, temp], axis='columns')

tt = comb_df.copy()
tt = comb_df.pct_change()
tt.dropna()

super_comb = pd.concat([btc, tt], axis='columns')
all_corr = super_comb.corr()

st.write("correlating BTC change rate with macro variables")
st.dataframe(all_corr)

st.write("""While they are not the main driving factors, an increase in fed fund rates does seem to result in a decrease in BTC prices.
The blue and green lines in the below plotconfirm this.""")

figx= plt.figure() 
plt.plot(btc.index, btc.BTC, label='BTC change rate')
plt.plot(super_comb.index, super_comb['UNRATE'], label='unemployment rate')
plt.plot(super_comb.index, super_comb['FEDFUNDS'], label='federal interest rate')
plt.legend(loc=0)
st.pyplot(figx)
st.write("""
Quick note: BTC change rate is scaled by 100 --> -0.5 = -50%, while others are not
""")
