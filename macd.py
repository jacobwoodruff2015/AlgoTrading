import pandas as pd
import streamlit as st
import yfinance as yf
import datetime
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from stockstats import StockDataFrame
from math import floor



def MACD(df,ticker):
    stock = StockDataFrame.retype(df)
    df['macd'] = stock['macd']

   
    def MACD_Strategy(df, risk):
        MACD_Buy=[]
        MACD_Sell=[]
        position=False

        for i in range(0, len(df)):
            if df['macd'][i] > df['macds'][i] :
                MACD_Sell.append(np.nan)
                if position ==False:
                    MACD_Buy.append(df['adj close'][i])
                    position=True
                else:
                    MACD_Buy.append(np.nan)
            elif df['macd'][i] < df['macds'][i] :
                MACD_Buy.append(np.nan)
                if position == True:
                    MACD_Sell.append(df['adj close'][i])
                    position=False
                else:
                    MACD_Sell.append(np.nan)
            elif position == True and df['adj close'][i] < MACD_Buy[-1] * (1 - risk):
                MACD_Sell.append(df["Adj Close"][i])
                MACD_Buy.append(np.nan)
                position = False
            elif position == True and df['adj close'][i] < df['adj close'][i - 1] * (1 - risk):
                MACD_Sell.append(df["adj close"][i])
                MACD_Buy.append(np.nan)
                position = False
            else:
                MACD_Buy.append(np.nan)
                MACD_Sell.append(np.nan)

        df['MACD_Buy_Signal_price'] = MACD_Buy
        df['MACD_Sell_Signal_price'] = MACD_Sell
    
    MACD_strategy = MACD_Strategy(df, 0.025)
    
    def MACD_color(df):
        MACD_color = []
        for i in range(0, len(df)):
            if df['macdh'][i] > df['macdh'][i - 1]:
                MACD_color.append(True)
            else:
                MACD_color.append(False)
        return MACD_color

    df['positive'] = MACD_color(df)

    def calculate_return(df):
        returns = []
        buy_price = None
        position = False
        for i in range(len(df)):
            if not np.isnan(df['MACD_Buy_Signal_price'][i]):
                buy_price = df['MACD_Buy_Signal_price'][i]
                position = True
            elif not np.isnan(df['MACD_Sell_Signal_price'][i]):
                if position:
                    returns.append((df['MACD_Sell_Signal_price'][i] - buy_price) / buy_price * 100)
                    position = False
        return sum(returns)

    return_percent = calculate_return(df)
    return_percent = round(return_percent,2)
    
    fig = make_subplots(rows=2,cols=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['adj close'],name='Adj Close Price',line=dict(color='skyblue')),row=1, col=1)

    fig.add_trace(go.Scatter(x=df.index, 
                                y=df['MACD_Buy_Signal_price'], name='Buy Signal', mode='markers',
                                marker=dict(color='green', size=8, symbol='triangle-up-dot')))
        
    fig.add_trace(go.Scatter(x=df.index, 
                                y=df['MACD_Sell_Signal_price'], name='Sell Signal', mode='markers',
                                marker=dict(color='red', size=8, symbol='triangle-down-dot')))

    
    
    
    fig.add_trace(go.Scatter(x=df.index, y=df['macds'],name='Signal',line=dict(color='yellow')), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['macd'],name='MACD',line=dict(color='red')), row=2, col=1)
        
    df["color"] = np.where(df["macdh"]<0, 'red', 'yellow')

    fig.add_trace(go.Bar(x=df.index,y=df['macdh'],marker_color=df['color'],showlegend=False), row=2, col=1)
            
    fig.update_layout(title=f"{ticker} MACD strategy",
                        xaxis_title='Timeframe',
                        yaxis_title='Adj Close Price')

    st.plotly_chart(fig,use_container_width=True)
    
    st.markdown(f'Profit percentage of the MACD strategy : **_{return_percent}%_**')
    
    

st.title('MACD Crossover strategy')
user_input = st.text_input('Enter The Stock Ticker', 'TATAPOWER.NS')

if st.button('Intraday'):
    df = yf.download(user_input, period='1d', interval='1m')
    MACD(df,user_input)

elif st.button('1Y'):
    df = yf.download(user_input, period='1y', interval='1d')
    MACD(df,user_input)
    
else:
    start = st.date_input('Enter Start date',datetime.date(2019,1, 1))
    end = st.date_input('Enter End date',datetime.date(2023,1, 1))
    df = yf.download(user_input, start=start, end=end)
    MACD(df,user_input)
