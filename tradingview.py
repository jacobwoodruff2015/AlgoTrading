from tradingview_ta import TA_Handler, Interval, Exchange, TradingView
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Wedge, Rectangle
st.set_page_config(layout="wide")


st.title('Technical Analysis')
ticker = st.text_input('Enter a Stock','RELIANCE')

interval = st.selectbox('Enter Interval',('1_MINUTE','15_MINUTES','30_MINUTES','1_HOUR','1_DAY','1_WEEK','1_MONTH'))

if interval =='15_MINUTES':
    a = TA_Handler(
        symbol = ticker,
        screener="india",
        exchange="NSE",
        interval=Interval.INTERVAL_15_MINUTES,
    )

elif interval =='1_MINUTE':
    a = TA_Handler(
        symbol = ticker,
        screener="india",
        exchange="NSE",
        interval=Interval.INTERVAL_1_MINUTE,
    )

elif interval == '30_MINUTES':
        a = TA_Handler(
        symbol = ticker,
        screener="india",
        exchange="NSE",
        interval=Interval.INTERVAL_30_MINUTES,
    )


elif interval == '1_HOUR':
        a = TA_Handler(
        symbol = ticker,
        screener="india",
        exchange="NSE",
        interval=Interval.INTERVAL_1_HOUR,
    )

elif interval == '1_WEEK':
        a = TA_Handler(
        symbol = ticker,
        screener="india",
        exchange="NSE",
        interval=Interval.INTERVAL_1_WEEK,
    )

elif interval == '1_DAY':
        a = TA_Handler(
        symbol = ticker,
        screener="india",
        exchange="NSE",
        interval=Interval.INTERVAL_1_DAY,
    )

elif interval == '1_MONTH':
        a = TA_Handler(
        symbol = ticker,
        screener="india",
        exchange="NSE",
        interval=Interval.INTERVAL_1_MONTH,
    )


# print(a.get_indicators())



o2 = a.get_indicators()
ma = ['EMA10','SMA10','EMA20','SMA20','EMA30','SMA30','EMA50','SMA50','EMA100','SMA100','EMA200','SMA200','Ichimoku.BLine','VWMA','HullMA9']
ma_val = []
for i,k in o2.items():
    if i in ma:
        ma_val.append(k)

df2 = pd.DataFrame()
df2['MA'] = ma
df2['Value'] = ma_val
df2['Action'] = a.get_analysis().moving_averages['COMPUTE'].values()
 
o1 = a.get_analysis().oscillators
r1 = ['Relative Strength Index (14)','Stochastic %K (14, 3, 3)','Commodity Channel Index (20)','Average Directional Index (14)','Awesome Oscillator','Momentum (10)','MACD Level (12, 26)','Stochastic RSI Fast (3, 3, 14, 14)','Williams Percent Range (14)','Bull Bear Power','Ultimate Oscillator (7, 14, 28)']
o_val=[o2['RSI'],o2['Stoch.K'],o2['CCI20'],o2['ADX'],o2['AO'],o2['Mom'],o2['MACD.macd'],
   o2['Stoch.RSI.K'],o2['W.R'],o2['BBPower'],o2['UO']]
df1 = pd.DataFrame()
df1['Oscillators'] = r1
df1['Value'] = o_val
df1['Action'] = o1['COMPUTE'].values()


sell_count = 0
buy_count = 0
neutral_count = 0

for i in range(len(df1)):
    if df1['Action'][i]=='BUY':
        buy_count+=1
    elif df1['Action'][i]=='SELL':
        sell_count+=1
    elif df1['Action'][i]=='NEUTRAL':
        neutral_count+=1

for i in range(len(df1)):
    if df2['Action'][i]=='BUY':
        buy_count+=1
    elif df2['Action'][i]=='SELL':
        sell_count+=1
    elif df2['Action'][i]=='NEUTRAL':
        neutral_count+=1  
        
        
def summary(sell,buy,neutral,ticker):
    em_5 = 'strong sell'
    em_4 = 'sell'
    em_3 = 'neutral'
    em_2 = 'buy'
    em_1 = 'strong buy'


    def degree_range(n): 
        start = np.linspace(0,180,n+1, endpoint=True)[0:-1]
        end = np.linspace(0,180,n+1, endpoint=True)[1::]
        mid_points = start + ((end-start)/2.)
        return np.c_[start, end], mid_points

    def rot_text(ang): 
        rotation = np.degrees(np.radians(ang) * np.pi / np.pi - np.radians(90))
        return rotation

    def gauge(labels=[ em_5, em_4, em_3, em_2, em_1],
            colors=['green','lightgreen','lightblue','#ffb09c','#ee2400'], 
            arrow="", 
            title="", 
            fname=False):     

        N = len(labels)
        
        if arrow > N: 
            raise Exception("\n\nThe category ({}) is greated than \
            the length\nof the labels ({})".format(arrow, N)) 
    
        # facecolor='black' to change the fig bg color
        fig, ax = plt.subplots(figsize=(7, 5))
        fig.subplots_adjust(0,0,2,1)

        ang_range, mid_points = degree_range(N)

        labels = labels[::-1]
        
        patches = []
        for ang, c in zip(ang_range, colors): 
            # sectors
            patches.append(Wedge((0.,0.), .4,*ang, facecolor='w', lw=2 ))
            # arcs
            patches.append(Wedge((0.,0.), .4,*ang, width=0.08, facecolor=c, lw=2, alpha=1,))
        
        # [ax.add_patch(p) for p in patches]
        
        for p in patches:
            ax.add_patch(p)

        for mid, lab in zip(mid_points, labels): 

            ax.text(0.42 * np.cos(np.radians(mid)), 0.42 * np.sin(np.radians(mid)), lab, \
                horizontalalignment='center', verticalalignment='center', fontsize=15, \
                rotation = rot_text(mid))


        r = Rectangle((-0.4,-0.1),0.8,0.1, facecolor='w', lw=2)
        ax.add_patch(r)
        
        ax.text(0, -0.1, title, horizontalalignment='center', \
            verticalalignment='center', fontsize=16 )


        
        pos = mid_points[abs(arrow - N)]
        
        ax.arrow(0, 0, 0.225 * np.cos(np.radians(pos)), 0.225 * np.sin(np.radians(pos)), \
                    width=0.01, head_width=0.01, head_length=0.05, fc='k', ec='k')
        
        ax.add_patch(Circle((0, 0), radius=0.02, facecolor='k'))
        ax.add_patch(Circle((0, 0), radius=0.01, facecolor='w', zorder=11))


        ax.set_frame_on(False)
        ax.axes.set_xticks([])
        ax.axes.set_yticks([])
        ax.axis('equal')
        
        
        # plt.tight_layout()
        # if fname:
        #     fig.savefig(fname, dpi=200)
        st.pyplot(fig)

    strong_buy = sell+neutral
    strong_sell = buy+neutral

    if buy == sell:
        arrow = 3
    else:
        if (buy >= sell) and (buy >= neutral):
            if ((strong_buy < buy) and (buy - strong_buy >=5) ):
                arrow = 5
            else:
                arrow = 4
        elif (sell >= buy) and (sell >= neutral):
            if ((strong_sell < sell) and (sell-strong_sell >=5) ):
                arrow = 1
            else:
                arrow = 2
        else:
            arrow = 3
            

    gauge(title= f'Technical Analysis for {ticker} Summary', arrow = arrow)

def oscillators(df,ticker):
    buy = 0
    sell = 0
    neutral = 0
    for i in range(len(df1)):
        if df['Action'][i]=='BUY':
            buy+=1
        elif df['Action'][i]=='SELL':
            sell+=1
        elif df['Action'][i]=='NEUTRAL':
            neutral+=1

    em_5 = 'strong sell'
    em_4 = 'sell'
    em_3 = 'neutral'
    em_2 = 'buy'
    em_1 = 'strong buy'


    def degree_range(n): 
        start = np.linspace(0,180,n+1, endpoint=True)[0:-1]
        end = np.linspace(0,180,n+1, endpoint=True)[1::]
        mid_points = start + ((end-start)/2.)
        return np.c_[start, end], mid_points

    def rot_text(ang): 
        rotation = np.degrees(np.radians(ang) * np.pi / np.pi - np.radians(90))
        return rotation

    def gauge(labels=[ em_5, em_4, em_3, em_2, em_1],
            colors=['green','lightgreen','lightblue','#ffb09c','#ee2400'], 
            arrow="", 
            title="", 
            fname=False):     

        N = len(labels)
        
        if arrow > N: 
            raise Exception("\n\nThe category ({}) is greated than \
            the length\nof the labels ({})".format(arrow, N)) 
    
        # facecolor='black' to change the fig bg color
        fig, ax = plt.subplots(figsize=(7, 5))
        fig.subplots_adjust(0,0,2,1)

        ang_range, mid_points = degree_range(N)

        labels = labels[::-1]
        
        patches = []
        for ang, c in zip(ang_range, colors): 
            # sectors
            patches.append(Wedge((0.,0.), .4,*ang, facecolor='w', lw=2 ))
            # arcs
            patches.append(Wedge((0.,0.), .4,*ang, width=0.08, facecolor=c, lw=2, alpha=1,))
        
        # [ax.add_patch(p) for p in patches]
        
        for p in patches:
            ax.add_patch(p)

        for mid, lab in zip(mid_points, labels): 

            ax.text(0.42 * np.cos(np.radians(mid)), 0.42 * np.sin(np.radians(mid)), lab, \
                horizontalalignment='center', verticalalignment='center', fontsize=15, \
                rotation = rot_text(mid))


        r = Rectangle((-0.4,-0.1),0.8,0.1, facecolor='w', lw=2)
        ax.add_patch(r)
        
        ax.text(0, -0.1, title, horizontalalignment='center', \
            verticalalignment='center', fontsize=16 )


        
        pos = mid_points[abs(arrow - N)]
        
        ax.arrow(0, 0, 0.225 * np.cos(np.radians(pos)), 0.225 * np.sin(np.radians(pos)), \
                    width=0.01, head_width=0.01, head_length=0.05, fc='k', ec='k')
        
        ax.add_patch(Circle((0, 0), radius=0.02, facecolor='k'))
        ax.add_patch(Circle((0, 0), radius=0.01, facecolor='w', zorder=11))


        ax.set_frame_on(False)
        ax.axes.set_xticks([])
        ax.axes.set_yticks([])
        ax.axis('equal')
        
        
        # plt.tight_layout()
        # if fname:
        #     fig.savefig(fname, dpi=200)
        st.pyplot(fig)

    strong_buy = sell+neutral
    strong_sell = buy+neutral

    if buy == sell:
        arrow = 3
    else:
        if (buy >= sell) and (buy >= neutral):
            if ((strong_buy < buy) and (buy - strong_buy >=5) ):
                arrow = 5
            else:
                arrow = 4
        elif (sell >= buy) and (sell >= neutral):
            if ((strong_sell < sell) and (sell-strong_sell >=5) ):
                arrow = 1
            else:
                arrow = 2
        else:
            arrow = 3
            

    gauge(title= f'Technical Analysis for {ticker} Oscillators', arrow = arrow)

def ma(df,ticker):
    buy = 0
    sell = 0
    neutral = 0
    for i in range(len(df1)):
        if df['Action'][i]=='BUY':
            buy+=1
        elif df['Action'][i]=='SELL':
            sell+=1
        elif df['Action'][i]=='NEUTRAL':
            neutral+=1

    em_5 = 'strong sell'
    em_4 = 'sell'
    em_3 = 'neutral'
    em_2 = 'buy'
    em_1 = 'strong buy'


    def degree_range(n): 
        start = np.linspace(0,180,n+1, endpoint=True)[0:-1]
        end = np.linspace(0,180,n+1, endpoint=True)[1::]
        mid_points = start + ((end-start)/2.)
        return np.c_[start, end], mid_points

    def rot_text(ang): 
        rotation = np.degrees(np.radians(ang) * np.pi / np.pi - np.radians(90))
        return rotation

    def gauge(labels=[ em_5, em_4, em_3, em_2, em_1],
            colors=['green','lightgreen','lightblue','#ffb09c','#ee2400'], 
            arrow="", 
            title="", 
            fname=False):     

        N = len(labels)
        
        if arrow > N: 
            raise Exception("\n\nThe category ({}) is greated than \
            the length\nof the labels ({})".format(arrow, N)) 
    
        # facecolor='black' to change the fig bg color
        fig, ax = plt.subplots(figsize=(7, 5))
        fig.subplots_adjust(0,0,2,1)

        ang_range, mid_points = degree_range(N)

        labels = labels[::-1]
        
        patches = []
        for ang, c in zip(ang_range, colors): 
            # sectors
            patches.append(Wedge((0.,0.), .4,*ang, facecolor='w', lw=2 ))
            # arcs
            patches.append(Wedge((0.,0.), .4,*ang, width=0.08, facecolor=c, lw=2, alpha=1,))
        
        # [ax.add_patch(p) for p in patches]
        
        for p in patches:
            ax.add_patch(p)

        for mid, lab in zip(mid_points, labels): 

            ax.text(0.42 * np.cos(np.radians(mid)), 0.42 * np.sin(np.radians(mid)), lab, \
                horizontalalignment='center', verticalalignment='center', fontsize=15, \
                rotation = rot_text(mid))


        r = Rectangle((-0.4,-0.1),0.8,0.1, facecolor='w', lw=2)
        ax.add_patch(r)
        
        ax.text(0, -0.1, title, horizontalalignment='center', \
            verticalalignment='center', fontsize=16 )


        
        pos = mid_points[abs(arrow - N)]
        
        ax.arrow(0, 0, 0.225 * np.cos(np.radians(pos)), 0.225 * np.sin(np.radians(pos)), \
                    width=0.01, head_width=0.01, head_length=0.05, fc='k', ec='k')
        
        ax.add_patch(Circle((0, 0), radius=0.02, facecolor='k'))
        ax.add_patch(Circle((0, 0), radius=0.01, facecolor='w', zorder=11))


        ax.set_frame_on(False)
        ax.axes.set_xticks([])
        ax.axes.set_yticks([])
        ax.axis('equal')
        
        
        # plt.tight_layout()
        # if fname:
        #     fig.savefig(fname, dpi=200)
        st.pyplot(fig)

    strong_buy = sell+neutral
    strong_sell = buy+neutral

    if buy == sell:
        arrow = 3
    else:
        if (buy >= sell) and (buy >= neutral):
            if ((strong_buy < buy) and (buy - strong_buy >=5) ):
                arrow = 5
            else:
                arrow = 4
        elif (sell >= buy) and (sell >= neutral):
            if ((strong_sell < sell) and (sell-strong_sell >=5) ):
                arrow = 1
            else:
                arrow = 2
        else:
            arrow = 3
            

    gauge(title= f'Technical Analysis for {ticker} Moving Averages', arrow = arrow)




st.subheader('Summary')
summary(sell_count,buy_count,neutral_count,ticker)

col1, col2 = st.columns(2)
with col1:
    st.subheader('Oscillators Technical Analysis')
    oscillators(df1,ticker)
    st.table(df1)

with col2:
    st.subheader('Moving Averages Technical Analysis')
    ma(df2,ticker)
    
    s1 = dict(selector='th', props=[('text-align', 'center')])
    s2 = dict(selector='td', props=[('text-align', 'center')])
    # you can include more styling paramteres, check the pandas docs
    table = df2.style.set_table_styles([s1,s2]).hide(axis=0).to_html()     
    st.markdown(table, unsafe_allow_html=True)
    # st.table(df2)

