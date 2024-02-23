from taipy.gui import Gui, notify
from datetime import date
import yfinance as yf
import pandas as pd
from keras.models import load_model
model = load_model('C:\\Users\\Sneha\\Desktop\\FitMate\\model.h5')
start_date = "2015-01-01"
end_date = date.today().strftime("%Y-%m-%d")
selected_stock = 'AAPL'
n_years = 1
def get_stock_data(ticker, start, end):
    ticker_data = yf.download(ticker, start, end)  
    ticker_data.reset_index(inplace=True)  
    ticker_data['Date'] = pd.to_datetime(ticker_data['Date']).dt.tz_localize(None)
    return ticker_data
def get_data_from_range(state):
    start_date = state.start_date if type(state.start_date) == str else state.start_date.strftime("%Y-%m-%d")
    end_date = state.end_date if type(state.end_date) == str else state.end_date.strftime("%Y-%m-%d")

    state.data = get_stock_data(state.selected_stock, start_date, end_date)
    if len(state.data) == 0:
        notify(state, "error",
               f"Not able to download data {state.selected_stock} from {start_date} to {end_date}")
        return
    notify(state, 's', 'Historical data has been updated!')
    notify(state, 'w', 'Deleting previous predictions...')
    state.forecast = pd.DataFrame(columns=['Date', 'Lower', 'Upper'])

def generate_forecast_data(data, n_years):
    historical_data = data['Close'].values.reshape(-1, 1) 
    prediction = model.predict(historical_data[-1:])  
    forecast_dates = pd.date_range(end=data['Date'].max(), periods=365 * n_years)
    lower = [prediction[0] - i * 2 for i in range(365 * n_years)]
    upper = [prediction[0] + i * 3 for i in range(365 * n_years)]
    forecast_data = pd.DataFrame({'Date': forecast_dates, 'Lower': lower, 'Upper': upper})
    return forecast_data
def forecast_display(state):
    notify(state, 'i', 'Predicting...')
    state.forecast = generate_forecast_data(state.data, state.n_years)
    notify(state, 's', 'Prediction done! Forecast data has been updated!')
data = get_stock_data(selected_stock, start_date, end_date)
forecast = generate_forecast_data(data, n_years)
show_dialog = False
partial_md = "<|{forecast}|table|>"
dialog_md = "<|{show_dialog}|dialog|partial={partial}|title=Forecast Data|on_action={lambda state: state.assign('show_dialog', False)}|>"
page = dialog_md + """<|toggle|theme|dark_mode=True|>
<|container style="background-color: #f0f0f0; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
# Stock Price **Analysis**{: .color-primary} Dashboard
<|layout|columns=1 2 1|gap=40px|class_name=card p2|
<dates style="margin-bottom: 20px;">
#### Selected **Period**{: .color-primary}
From:
<|{start_date}|date|on_change=get_data_from_range|>  
To:
<|{end_date}|date|on_change=get_data_from_range|> 
|dates>
<ticker style="margin-bottom: 20px;">
#### Selected **Ticker**{: .color-primary}
Please enter a valid ticker: 
<|{selected_stock}|input|label=Stock|on_action=get_data_from_range|> 
or choose a popular one
<|{selected_stock}|toggle|lov=MSFT;GOOG;AAPL; AMZN; META; COIN; AMC; PYPL|on_change=get_data_from_range|>
|ticker>
<years style="margin-bottom: 20px;">
#### Prediction **years**{: .color-primary}
Select number of prediction years: <|{n_years}|>  
<|{n_years}|slider|min=1|max=5|>  
<|PREDICT|button|on_action=forecast_display|class_name={'plain' if len(forecast)==0 else ''}|>
|years>
|>
<|Historical Data|expandable|expanded=False| style="margin-bottom: 20px;">
<|layout|columns=1 1|
<|
### Historical **closing**{: .color-primary} price
<|{data}|chart|mode=line|x=Date|y[1]=Open|y[2]=Close|>
|>
<|
### Historical **daily**{: .color-primary} trading volume
<|{data}|chart|mode=line|x=Date|y=Volume|>
|>
|>
### **Whole**{: .color-primary} historical data: <|{selected_stock}|text|raw|>
<|{data}|table|>
<br/>
|>
### **Forecast**{: .color-primary} Data
<|{forecast}|chart|mode=line|x=Date|y[1]=Lower|y[2]=Upper|>
<br/>
<|More info|button|on_action={lambda s: s.assign("show_dialog", True)}|>
{: .text-center}
|>
<br/>
"""
ui = Gui(page)
partial = gui.add_partial(partial_md)
gui.run(dark_mode=True, title="Stock Visualization")
