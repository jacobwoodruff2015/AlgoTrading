import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf
import datetime
import plotly.express as px


def sMA(df,ticker):
    m1 = st.number_input('Enter Moving Average 1:- ',value=50)
    m2 = st.number_input('Enter Moving Average 2:- ',value=200)
    df['ma_1'] = df['Adj Close'].rolling(m1).mean()
    df['ma_2'] = df['Adj Close'].rolling(m2).mean()
    df = df.dropna()
    df = df[['Adj Close', 'ma_1', 'ma_2']]
    Buy = []
    Sell = []
    buyprices = []
    sellprices = []

    for i in range(len(df)):
        if df.ma_1.iloc[i] > df.ma_2.iloc[i] \
        and df.ma_1.iloc[i-1] < df.ma_2.iloc[i-1]:
            Buy.append(i)
            buyprices.append(df.iloc[i]['Adj Close'])
        elif df.ma_1.iloc[i] < df.ma_2.iloc[i] \
        and df.ma_1.iloc[i-1] > df.ma_2.iloc[i-1]:
            Sell.append(i)
            sellprices.append(df.iloc[i]['Adj Close'])
    
    
    
    fig = make_subplots(rows=1, cols=1)
    
    fig.add_trace(go.Scatter(x=df.index, y=df['Adj Close'],name='Adj Close Price'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['ma_1'], name=f'MA{m1}'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['ma_2'], name=f'MA {m2}'), row=1, col=1)
    
    fig.add_trace(go.Scatter(x=df.iloc[Buy].index, 
                             y=df['Adj Close'], name='Buy Signal', mode='markers',
                            marker=dict(color='green', size=8, symbol='triangle-up-dot')))
    
    fig.add_trace(go.Scatter(x=df.iloc[Sell].index, 
                             y=df['Adj Close'], name='Sell Signal', mode='markers',
                            marker=dict(color='red', size=8, symbol='triangle-down-dot')))
    
    fig.update_layout(title=f"{ ticker } stock SMA Crossover strategy",
                  xaxis_title='Timeframe',
                  yaxis_title='Adj Close Price')
           
    st.plotly_chart(fig)
    
    
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

else:
    start = st.date_input('Enter start date',datetime.date(2019,1, 1))
    end = st.date_input('Enter end date',datetime.date(2022,1, 1))
    df = yf.download(user_input, start=start, end=end)
    
sMA(df,user_input)






