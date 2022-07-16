import  streamlit as st

st.title('Future Plans')

st.success("""
We plan to continue with this project.
- Add more backtesting features
- Use more of the data we gathered
- Add ML algorithms to predict future returns
- make technical analysis more customisable & interactive

""")

st.subheader("Quick explanation of notebooks uploaded")
st.error("""
- create_db: creates a database, and tables using SQL
- pop_db: populate the database and tables after creating them eith create_db.
- to_sql: In the end, this was used to populate the database from parquet files.
- get_data: gets relevant data from Alpaca, FRED, Quandl, etc., and saves them all as parquet files.
- get_sentiment: Obtains news for each cryptocurrency from API, then uses transformers and cryptoBERT to analyse the sentiment.
- get_ts: gets a tear sheet for each cryptocurrency. Replace 'BTC-USD' with 'ETH-USD' for example, to get tear sheets for other cryptos. the ticker code is the ones used by yahoo finance.
- get_tv: gets the current sentiment of a crypto from tradingview.
- make_plots: to create plotly graphs. They are interactive.


""")
