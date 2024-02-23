from taipy.gui import Gui
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import io
import warnings

warnings.filterwarnings('ignore')

# Function to compute RSI
def compute_rsi(data, time_window):
    diff = data.diff(1)
    gain = (diff.where(diff > 0, 0)).rolling(window=time_window).mean()
    loss = (-diff.where(diff < 0, 0)).rolling(window=time_window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Load cryptocurrency data from URLs

def load_crypto_data(urls, start_date):
    crypto_data = {}
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            crypto_name = url.split("/")[-1].split("_")[1].split(".")[0]
            df = pd.read_csv(io.StringIO(response.text))
            # Rename columns to lowercase and remove spaces
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            print(f"Columns in DataFrame for {crypto_name}: {df.columns}")
            # Ensure 'date' column exists and is in datetime format
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            elif 'unix' in df.columns:  # Some data might have 'unix' column instead of 'date'
                df['date'] = pd.to_datetime(df['unix'], unit='ms')
            else:
                raise KeyError("Date column not found in DataFrame")
            df.set_index('date', inplace=True)
            df = df.loc[start_date:]
            df['rsi'] = compute_rsi(df['close'], 14)  # Adjust RSI time window if needed
            crypto_data[crypto_name] = df
    return crypto_data

# URLs of cryptocurrency data
urls = [
    "https://www.cryptodatadownload.com/cdd/Bitfinex_EOSUSD_d.csv", 
    "https://www.cryptodatadownload.com/cdd/Bitfinex_EDOUSD_d.csv",
    "https://www.cryptodatadownload.com/cdd/Bitfinex_BTCUSD_d.csv",
    "https://www.cryptodatadownload.com/cdd/Bitfinex_ETHUSD_d.csv",
    "https://www.cryptodatadownload.com/cdd/Bitfinex_LTCUSD_d.csv",
    "https://www.cryptodatadownload.com/cdd/Bitfinex_BATUSD_d.csv",
    "https://www.cryptodatadownload.com/cdd/Bitfinex_OMGUSD_d.csv",
    "https://www.cryptodatadownload.com/cdd/Bitfinex_DAIUSD_d.csv",
    "https://www.cryptodatadownload.com/cdd/Bitfinex_ETCUSD_d.csv",
    "https://www.cryptodatadownload.com/cdd/Bitfinex_ETPUSD_d.csv",
    "https://www.cryptodatadownload.com/cdd/Bitfinex_NEOUSD_d.csv",
    "https://www.cryptodatadownload.com/cdd/Bitfinex_REPUSD_d.csv",
     "https://www.cryptodatadownload.com/cdd/Bitfinex_TRXUSD_d.csv",
     "https://www.cryptodatadownload.com/cdd/Bitfinex_XLMUSD_d.csv",
    "https://www.cryptodatadownload.com/cdd/Bitfinex_XMRUSD_d.csv",
     "https://www.cryptodatadownload.com/cdd/Bitfinex_XVGUSD_d.csv", 
]

# Start date for historical data
start_date = "2021-01-01"

# Load cryptocurrency data
crypto_data = load_crypto_data(urls, start_date)

# Create subplot
fig = make_subplots(rows=len(crypto_data), cols=1, shared_xaxes=True, subplot_titles=list(crypto_data.keys()))

# Add traces for each cryptocurrency
for i, (crypto_name, df) in enumerate(crypto_data.items(), start=1):
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close'), row=i, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], mode='lines', name='RSI'), row=i, col=1)

# Update layout
fig.update_layout(title="Cryptocurrency Dashboard", showlegend=False)

# Create GUI instance
gui = Gui(fig)

# Set initial state
gui.start_date = start_date

# Run GUI
gui.run(title="Cryptocurrency Dashboard")
