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

    def implement_macd_strategy(prices, data):    
        buy_price = []
        sell_price = []
        macd_signal = []
        signal = 0

        for i in range(len(data)):
            if data['macd'][i] > data['macds'][i]:
                if signal != 1:
                    buy_price.append(prices[i])
                    sell_price.append(np.nan)
                    signal = 1
                    macd_signal.append(signal)
                else:
                    buy_price.append(np.nan)
                    sell_price.append(np.nan)
                    macd_signal.append(0)
            elif data['macd'][i] < data['macds'][i]:
                if signal != -1:
                    buy_price.append(np.nan)
                    sell_price.append(prices[i])
                    signal = -1
                    macd_signal.append(signal)
                else:
                    buy_price.append(np.nan)
                    sell_price.append(np.nan)
                    macd_signal.append(0)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
                
        return buy_price, sell_price, macd_signal
            
    buy_price, sell_price, macd_signal = implement_macd_strategy(df['close'], stock)
    
    
    position = []
    for i in range(len(macd_signal)):
        if macd_signal[i] > 1:
            position.append(0)
        else:
            position.append(1)
            
    for i in range(len(df['close'])):
        if macd_signal[i] == 1:
            position[i] = 1
        elif macd_signal[i] == -1:
            position[i] = 0
        else:
            position[i] = position[i-1]
            
    macd = df['macd']
    signal = df['macds']
    close_price = df['close']
    macd_signal = pd.DataFrame(macd_signal).rename(columns = {0:'macd_signal'}).set_index(df.index)
    position = pd.DataFrame(position).rename(columns = {0:'macd_position'}).set_index(df.index)

    frames = [close_price, macd, signal, macd_signal, position]
    strategy = pd.concat(frames, join = 'inner', axis = 1)
    
    
    
    
    
    fig = make_subplots(rows=2, cols=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['adj close'],name='Adj Close Price',line=dict(color='skyblue')),row=1, col=1)
    
    
    fig.add_trace(go.Scatter(x=df.index, 
                             y=buy_price, name='Buy Signal', mode='markers',
                            marker=dict(color='green', size=8, symbol='triangle-up-dot')))
    
    fig.add_trace(go.Scatter(x=df.index, 
                             y=sell_price, name='Sell Signal', mode='markers',
                            marker=dict(color='red', size=8, symbol='triangle-down-dot')))
    

    fig.add_trace(go.Scatter(x=df.index, y=df['macds'],name='Signal',line=dict(color='yellow')), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['macd'],name='MACD',line=dict(color='red')), row=2, col=1)
        
    df["color"] = np.where(df["macdh"]<0, 'red', 'yellow')

    fig.add_trace(go.Bar(x=df.index,y=df['macdh'],marker_color=df['color']), row=2, col=1)
            
    fig.update_layout(title=f"{ticker} MACD strategy",
                        xaxis_title='Timeframe',
                        yaxis_title='Adj Close Price')

    st.plotly_chart(fig,use_container_width=True)




    stock_ret = pd.DataFrame(np.diff(df['close'])).rename(columns = {0:'returns'})
    
    macd_strategy_ret = []

    for i in range(len(stock_ret)):
        try:
            returns = stock_ret['returns'][i]*strategy['macd_position'][i]
            macd_strategy_ret.append(returns)
        except:
            pass
        
    macd_strategy_ret_df = pd.DataFrame(macd_strategy_ret).rename(columns = {0:'macd_returns'})

    investment_value = 1000
    number_of_stocks = floor(investment_value/df['close'][0])
    macd_investment_ret = []

    for i in range(len(macd_strategy_ret_df['macd_returns'])):
        returns = number_of_stocks*macd_strategy_ret_df['macd_returns'][i]
        macd_investment_ret.append(returns)

    macd_investment_ret_df = pd.DataFrame(macd_investment_ret).rename(columns = {0:'investment_returns'})
    total_investment_ret = round(sum(macd_investment_ret_df['investment_returns']), 2)
    profit_percentage = floor((total_investment_ret/investment_value)*100)
    
    st.markdown('Profit gained from the MACD strategy by investing 1000 Rs in : **_{}_**'.format(total_investment_ret))
    st.markdown('Profit percentage of the MACD strategy : **_{}%_**'.format(profit_percentage))


st.title('MACD Crossover strategy')
user_input = st.text_input('Enter The Stock Ticker', 'TATAPOWER.NS')

if st.button('Intraday'):
    df = yf.download(tickers=user_input, period='1d', interval='1m')

else:
    start = st.date_input('Enter Start date',datetime.date(2019,1, 1))
    end = st.date_input('Enter End date',datetime.date(2023,1, 1))
    df = yf.download(user_input, start=start, end=end)
    
MACD(df,user_input)
