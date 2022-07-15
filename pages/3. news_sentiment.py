import  streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect('./test.db')

st.title('News Sentiment')

s_lab = st.selectbox("Choose a sentiment:", ["All", 'Bullish', "Neutral", "Bearish"], )
coin_name = st.selectbox("Choose a Coin:", ["BTCUSD", "BCHUSD", "ETHUSD", "LTCUSD", "DOGEUSD", "USDTUSD"])
df2 = pd.read_sql(sql=f"""select * from crypto_news where sentiment_label = '{s_lab}' and coin = '{coin_name}'
;""", con=conn)

if s_lab == "All":
    df2 = pd.read_sql(sql=f"""select * from crypto_news where coin = '{coin_name}';""", con=conn)

st.dataframe(df2)

if st.button("Show All News:"):
    df = pd.read_sql(sql=f"""select * from crypto_news;""", con=conn)

    st.dataframe(df)
