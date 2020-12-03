import streamlit as st
import pandas as pd
import datetime as dt
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
import time
from crypto_coin import Coin
import data_plot

# body_html = """
#     <style>
#         body { 
#             background-color: #282c34;
#             color: #ff48c4;
#         }

#         .sidebar .sidebar-content { 
#             background-color: #282c34;
#         }
#     </style>

# """
# st.markdown(body_html, unsafe_allow_html=True)
st.write("""
# Crypto Currency Dashboard

*see sidebar to the left for more info*
""")

st.sidebar.write("## Guide")
st.sidebar.write("""
- select coin(s) you would like data for
- select the currency you wish to use
- select a range of dates (this is for the candle stick plot)
""")

st.sidebar.write("## Info")
st.sidebar.write("""
- candle stick plot(s) -- default date range is last 30 days
- 24 hour stats for the selected coins(s)
- the order book for the selected coin(s)
- the ticker for the selected coin(s)
""")

coin_col, currency_col = st.beta_columns(2)

coins = coin_col.multiselect('Check the cryptos you want to watch', ['BTC', 'ETH', 'ETC', 'XRP', 'LTC', 'ATOM', 'LINK', 'ALGO', 'OMG'])
currency = currency_col.selectbox('Choose a currency', ['USD', 'EUR', 'GBP'])


date_picker = st.date_input('Choose Date Range', [dt.date.today() - dt.timedelta(days=30), dt.date.today() + dt.timedelta(days=1)], min_value=dt.date.today() - dt.timedelta(days=365), max_value=dt.date.today() + dt.timedelta(days=1))


date_list = []
increment_date = date_picker[1]
while increment_date != date_picker[0]:
    increment_date -= dt.timedelta(days=1)
    date_list.append(increment_date)


# format_string = coin_symbol + '-' + currency
# append the currency to each coin in the list
for i in range(len(coins)):
    coins[i] = coins[i] + '-' + currency


# populate a coin list
coin_list = []
for coin in coins:
    new_coin = Coin(coin, date_picker[0], date_picker[1])
    coin_list.append(new_coin)


display_data = {}
rename = {}
if len(coin_list) != 0:
    k = 0
    for coin in coin_list:
        # set up key and assign empty list in dictionary
        key = coin.get_coin_name()
        display_data.setdefault(key, [])

        rename[0] = key

        history = data_plot.get_historic_info(coin.get_coin_name(), date_picker[0], date_picker[1], 86400)
        data_frame_of_history = pd.DataFrame(history)
        fig = go.FigureWidget(data=[go.Candlestick(x=date_list,
                low=data_frame_of_history[1],
                high=data_frame_of_history[2],
                open=data_frame_of_history[3],
                close=data_frame_of_history[4])])
        
        fig.update_layout(
            title=coin.get_coin_name() +' stock price',
            yaxis_title=coin.get_coin_name() +' price',
            xaxis_title='Date'
        )

        display_data[key].append(fig)

        daily_stats = data_plot.twent_four_hr_info(coin.get_coin_name())
        data_frame_of_stats = pd.DataFrame(daily_stats, index=[0])
        data_frame_of_stats = data_frame_of_stats.T.rename(rename, axis='columns')
        display_data[key].append(data_frame_of_stats) 

        order_book = data_plot.order_book_info(coin.get_coin_name())
        data_frame_of_order_book = pd.DataFrame(order_book, index=[0])
        data_frame_of_order_book = data_frame_of_order_book.T.rename(rename, axis='columns')
        display_data[key].append(data_frame_of_order_book)

        ticker = data_plot.ticker_info(coin.get_coin_name())
        data_frame_of_ticker = pd.DataFrame(ticker, index=[0])
        data_frame_of_ticker = data_frame_of_ticker.T.rename(rename, axis='columns')
        display_data[key].append(data_frame_of_ticker)

        k += 1
    
    for key in display_data:
        st.write("## " + key)
        st.plotly_chart(display_data[key][0], use_container_width=True)

        coin_info = st.beta_expander("More info for - " + key)
        coin_info.write("### 24hr Stats:")
        coin_info.write(display_data[key][1])

        coin_info.write("### Order Book:")
        coin_info.write(display_data[key][2])

        coin_info.write("### Ticker Info:")
        coin_info.write(display_data[key][3])
