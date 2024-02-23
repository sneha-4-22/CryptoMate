from taipy.gui import Gui
from datetime import date
import yfinance as yf
from PIL import Image
import base64

def get_crypto_data(coin, start_date, end_date):
    data = yf.download(coin, start=start_date, end=end_date)
    return data

start_date = "2023-09-01"
end_date = date.today().strftime("%Y-%m-%d")
BTC = get_crypto_data('BTC-USD', start_date, end_date)
ETH = get_crypto_data('ETH-USD', start_date, end_date)
XRP = get_crypto_data('XRP-USD', start_date, end_date)
BCH = get_crypto_data('BCH-USD', start_date, end_date)
BTC_his = yf.download('BTC-USD', start=start_date, end=end_date)
ETH_his = yf.download('ETH-USD', start=start_date, end=end_date)
XRP_his = yf.download('XRP-USD', start=start_date, end=end_date)
BCH_his = yf.download('BCH-USD', start=start_date, end=end_date)

imageBTC = Image.open('1.png')
imageETH = Image.open('2.png')
imageXRP = Image.open('3.png')
imageBCH = Image.open('4.png')

# # Convert images to base64 strings
# imageBTC_base64 = base64.b64encode(imageBTC.tobytes()).decode('utf-8')
# imageETH_base64 = base64.b64encode(imageETH.tobytes()).decode('utf-8')
# imageXRP_base64 = base64.b64encode(imageXRP.tobytes()).decode('utf-8')
# imageBCH_base64 = base64.b64encode(imageBCH.tobytes()).decode('utf-8')

page = """
<|container style="background-color: #F0F8FF;">
# Crypto Daily Prices

<|part|
## Main Dashboard
#### Add more crypto in code
|part>

<|layout|columns=2|class_name=card|
<crypto1|
## BITCOIN ($)
<|{imageBTC}|image|>
<|{BTC}|table|>
<|{BTC_his}|chart|mode=line|title=Historical Prices|>
|crypto1>

<crypto2|
## ETHEREUM ($)
<|{imageETH}|image|>
<|{ETH}|table|>
<|{ETH_his}|chart|mode=line|title=Historical Prices|>
|crypto2>

<crypto3|
## RIPPLE ($)
<|{imageXRP}|image|>
<|{XRP}|table|>
<|{XRP_his}|chart|mode=line|title=Historical Prices|>
|crypto3>

<crypto4|
## BITCOINCASH ($)
<|{imageBCH}|image|>
<|{BCH}|table|>
<|{BCH_his}|chart|mode=line|title=Historical Prices|>
|crypto4>
|layout>
</container>
"""

# Create the GUI instance
gui = Gui(page)

# Set initial state
gui.start_date = start_date
gui.end_date = end_date
gui.BTC = BTC
gui.ETH = ETH
gui.XRP = XRP
gui.BCH = BCH
gui.BTC_his = BTC_his
gui.ETH_his = ETH_his
gui.XRP_his = XRP_his
gui.BCH_his = BCH_his

# Run the GUI
gui.run(title="Crypto Daily Prices")
