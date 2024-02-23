from taipy.gui import Gui, notify
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Function to fetch cryptocurrency data
def get_crypto_data(coin, start_date, end_date):
    data = yf.download(coin, start=start_date, end=end_date)
    return data

# Function to plot cryptocurrency data
def plot_crypto_data(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['Close'], label='Closing Price')
    plt.title('Cryptocurrency Historical Prices')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.show()

# Define the start and end dates
start_date = "2015-01-01"
end_date = date.today().strftime("%Y-%m-%d")

# Initial cryptocurrency selection
selected_crypto = 'BTC-USD'

# Fetch cryptocurrency data
crypto_data = get_crypto_data(selected_crypto, start_date, end_date)

# Plot cryptocurrency data
plot_crypto_data(crypto_data)

# Define the layout page
page = """
<|container style="background-color: #F0F8FF;">
# Cryptocurrency Historical Prices

<|part|crypto_selection style="margin-bottom: 20px;">
#### Select Cryptocurrency:
<|{selected_crypto}|input|label=Symbol|on_action=get_crypto_data|>
|crypto_selection>
<br/>

### **Historical** Prices
<|{plot_crypto_data}|chart|>
<br/>
"""

# Create the GUI instance
gui = Gui(page)

# Function to update cryptocurrency data based on user input
def get_crypto_data(state):
    selected_crypto = state.selected_crypto.upper()
    crypto_data = get_crypto_data(selected_crypto, start_date, end_date)
    state.plot_crypto_data = crypto_data

# Add the function to the GUI
gui.add_action('get_crypto_data', get_crypto_data)

# Add the partial for plotting cryptocurrency data
gui.add_partial(plot_crypto_data)

# Run the GUI
gui.run(title="Cryptocurrency Analysis")
