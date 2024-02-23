import yfinance as yf
import streamlit as st
from PIL import Image
from urllib.request import urlopen   


# Titles and subtitles
st.title("Crypto Daily Prices")
st.header("Main Dashboard")
st.subheader("Add more crypto in code")


# Define ticker variables
Bitcoin = 'BTC-USD'
Ethereum = 'ETH-USD'
Ripple = 'XRP-USD'
BitcoinCash = 'BCH-USD'

# Fetch data from Yahoo Finance
BTC_data = yf.Ticker(Bitcoin)
ETH_data = yf.Ticker(Ethereum)
XRP_data = yf.Ticker(Ripple)
BCH_data = yf.Ticker(BitcoinCash)

# Fetch history data from Yahoo Finance
BTC_his = BTC_data.history(period="max")
ETH_his = ETH_data.history(period="max")
XRP_his = XRP_data.history(period="max")
BCH_his = BCH_data.history(period="max")

# Fetch data from dataframe
BTC = yf.download(Bitcoin, start="2023-09-01", end="2023-09-02")
ETH = yf.download(Ethereum, start="2023-09-01", end="2023-09-02")
XRP = yf.download(Ripple, start="2023-09-01", end="2023-09-02")
BCH = yf.download(BitcoinCash, start="2023-09-01", end="2023-09-02")

# Bitcoin
st.write("BITCOIN ($)")

# Fetch and display image
imageBTC = Image.open(
    urlopen('https://s2.coinmarketcap.com/static/img/coins/64x64/1.png'))
st.image(imageBTC)

# Display dataframe
st.table(BTC)

# Display a chart
st.bar_chart(BTC_his.Close)
#######################################

# Ethereum
st.write("ETHEREUM ($)")

# Fetch and display image
imageETH = Image.open(
    urlopen('https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png'))
st.image(imageETH)

# Display dataframe
st.table(ETH)

# Display a chart
st.bar_chart(ETH_his.Close)
################################################

# Ripple
st.write("RIPPLE ($)")

# Fetch and display image
imageXRP = Image.open(
    urlopen('https://s2.coinmarketcap.com/static/img/coins/64x64/52.png'))
st.image(imageXRP)

# Display dataframe
st.table(XRP)

# Display a chart
st.bar_chart(XRP_his.Close)
################################################


# BitcoinCash
st.write("BITCOINCASH ($)")

# Fetch and display image
imageBCH = Image.open(
    urlopen('https://s2.coinmarketcap.com/static/img/coins/64x64/1831.png'))
st.image(imageBCH)

# Display dataframe
st.table(BCH)

# Display a chart
st.bar_chart(BCH_his.Close)
################################################