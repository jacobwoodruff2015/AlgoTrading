import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf
import datetime
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import stockstats

def sMA(df,ticker):
    m1 = st.number_input('Enter Moving Average 1:- ',value=50)
    m2 = st.number_input('Enter Moving Average 2:- ',value=200)
    # df['ma_1'] = df['Close'].rolling(m1).mean()
    # df['ma_2'] = df['Close'].rolling(m2).mean()
    stock = stockstats.StockDataFrame.retype(df)
    # Calculate 13-day and 50-day SMA
    df["ma_1"] = stock.get(f"close_{m1}_sma")
    df["ma_2"] = stock.get(f"close_{m2}_sma")
    df = df.dropna()
    df = df[['close', 'ma_1', 'ma_2']]
    Buy = []
    Sell = []
    buyprices = []
    sellprices = []

    for i in range(len(df)):
        if df.ma_1.iloc[i] > df.ma_2.iloc[i] \
        and df.ma_1.iloc[i-1] < df.ma_2.iloc[i-1]:
            Buy.append(i)
            buyprices.append(df.iloc[i]['close'])
        elif df.ma_1.iloc[i] < df.ma_2.iloc[i] \
        and df.ma_1.iloc[i-1] > df.ma_2.iloc[i-1]:
            Sell.append(i)
            sellprices.append(df.iloc[i]['close'])
    
    if Buy[0] > Sell[0]:
        Sell.pop(0)
        sellprices.pop(0)
    if Buy[len(Buy)-1] > Sell[len(Sell)-1]:
        Buy.pop()
        buyprices.pop
        
    fig = make_subplots(rows=1, cols=1)
    
    fig.add_trace(go.Scatter(x=df.index, y=df['close'],name='close Price'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['ma_1'], name=f'MA{m1}'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['ma_2'], name=f'MA {m2}'), row=1, col=1)
    
    fig.add_trace(go.Scatter(x=df.iloc[Buy].index, 
                             y=df.iloc[Buy]['close'], name='Buy Signal', mode='markers',
                            marker=dict(color='green', size=8, symbol='triangle-up-dot')))
    
    fig.add_trace(go.Scatter(x=df.iloc[Sell].index, 
                             y=df.iloc[Sell]['close'], name='Sell Signal', mode='markers',
                            marker=dict(color='red', size=8, symbol='triangle-down-dot')))
    
    fig.update_layout(title=f"{ ticker } stock SMA Crossover strategy",
                  xaxis_title='Timeframe',
                  yaxis_title='close Price')
           
    st.plotly_chart(fig,use_container_width=True)
    
    
    
    a = ((pd.Series([(sell - buy) / buy for sell, buy in zip(sellprices, buyprices)]) + 1).prod() - 1) * 100
    
    a = str(round(a,2))
    
    st.subheader('Total Buy signals:- '+str(len(Buy)))
    st.subheader('Total Sell signals:- '+str(len(Sell)))
    st.subheader('Final percentage gain:-   '+a+'%')
    

    
#Load stock data
st.title('Simple Moving Average')
user_input = st.text_input('Enter The Stock Ticker', 'TATAPOWER.NS')

if st.button('Intraday'):
    df = yf.download(tickers=user_input, period='1d', interval='1m')
    sMA(df,user_input)
    
elif st.button('1Y'):
    df = yf.download(user_input, period='1y', interval='1d')
    sMA(df,user_input)
else:
    start = st.date_input('Enter Start date',datetime.date(2019,1, 1))
    end = st.date_input('Enter End date',datetime.date(2023,1, 1))
    df = yf.download(user_input, start=start, end=end)
    sMA(df,user_input)





