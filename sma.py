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
    
    
    
    f = plt.figure()
    f.set_figwidth(15)
    f.set_figheight(5)
    plt.suptitle(f"{ ticker } stock SMA Crossover strategy")
    plt.plot(df['Adj Close'], label = 'Asset Price', c = 'blue', alpha = 0.5)
    plt.plot(df['ma_1'], label = f'MA {m1}', c = 'k', alpha = 0.9)
    plt.plot(df['ma_2'], label = f'MA {m2}', c = 'magenta', alpha = 0.9)
    plt.scatter(df.iloc[Buy].index, df.iloc[Buy]['Adj Close'], marker = '^', color = 'g', s = 100)
    plt.scatter(df.iloc[Sell].index, df.iloc[Sell]['Adj Close'], marker = 'v', color = 'r', s = 100)
    plt.xlabel('Timeframe')
    plt.ylabel('Adj Close price')
    plt.legend()
    st.pyplot(f)
    
    a = ((pd.Series([(sell - buy) / buy for sell, buy in zip(sellprices, buyprices)]) + 1).prod() - 1) * 100
    
    a = str(round(a,2))
    
    st.subheader('Total Buy signals:- '+str(len(Buy)))
    st.subheader('Total Sell signals:- '+str(len(Sell)))
    st.subheader('Final percentage gain:-   '+a+'%')
    

    
#Load stock data
st.title('Simple Moving Average')
user_input = st.text_input('Enter The Stock Ticker', 'TATAPOWER.NS')
start = st.date_input('Enter end date',datetime.date(2019,1, 1))
end = st.date_input('Enter end date',datetime.date(2022,1, 1))
df = yf.download(user_input, start=start, end=end)
sMA(df,user_input)






