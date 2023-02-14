import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf
import datetime
import plotly.express as px
import ta 
import numpy as np


def bollingerRSI(df,ticker):
    
    df['ma_20'] = df.Close.rolling(20).mean()
    df['vol'] = df.Close.rolling(20).std()
    df['upper_bb'] = df.ma_20 + (2 * df.vol)
    df['lower_bb'] = df.ma_20 - (2 * df.vol)
    df['rsi'] = ta.momentum.rsi(df.Close, window=6)
    conditions = [(df.rsi < 30) & (df.Close < df.lower_bb), (df.rsi > 70) & (df.Close > df.upper_bb)]
    choices = ['Buy', 'Sell']
    df['signal'] = np.select(conditions, choices)
    df.dropna(inplace=True)
    df.signal = df.signal.shift()
    position = False
    buydates, selldates = [],[]
    buyprices, sellprices = [],[]

    for index, row in df.iterrows():
        if not position and row['signal'] == 'Buy':
            buydates.append(index)
            buyprices.append(row.Open)
            position = True
        
        if position and row['signal'] == 'Sell':
            selldates.append(index)
            sellprices.append(row.Open)
            position = False

    f = plt.figure()
    f.set_figwidth(15)
    f.set_figheight(5)
    plt.suptitle(f"{ ticker } stock Bollinger X RSI Crossover strategy")
    plt.plot(df['Adj Close'], label = 'Asset Price', c = 'blue', alpha = 0.5)
    # plt.plot(df['upper_bb'], label = f'Upper BB', c = 'k', alpha = 0.9)
    # plt.plot(df['lower_bb'], label = f'Lower BB', c = 'magenta', alpha = 0.9)
    plt.scatter(df.loc[buydates].index, df.loc[buydates].Close, marker = "^", c = 'g',label='Buy')
    plt.scatter(df.loc[selldates].index, df.loc[selldates].Close, marker = "v", c = 'r',label='Sell')
    plt.xlabel('Timeframe')
    plt.ylabel('Adj Close price')
    plt.legend()
    st.pyplot(f)
    
    a = ((pd.Series([(sell - buy) / buy for sell, buy in zip(sellprices, buyprices)]) + 1).prod() - 1) * 100
    
    a = str(round(a,2))

    st.subheader('Total Buy signals:- '+str(len(buyprices)))
    st.subheader('Total Sell signals:- '+str(len(sellprices)))
    st.subheader('Final percentage gain:-   '+a+'%')
    

    
#Load stock data
st.title('Bollinger X RSI trading strategy')
user_input = st.text_input('Enter The Stock Ticker', 'HDFC.NS')

if st.button('Intraday'):
    df = yf.download(tickers=user_input, period='1d', interval='1m')
    bollingerRSI(df,user_input)
    
elif st.button('1Y'):
    df = yf.download(user_input, period='1y', interval='1d')
    sMA(df,user_input)
    bollingerRSI(df,user_input)
else:
    start = st.date_input('Enter end date',datetime.date(2019,1, 1))
    end = st.date_input('Enter end date',datetime.date(2022,1, 1))
    df = yf.download(user_input, start=start, end=end)
    bollingerRSI(df,user_input)






