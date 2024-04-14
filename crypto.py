import pandas as pd
from taipy.gui import Gui, notify
import numpy as np
df = pd.read_csv("C:\\Users\\Sneha\\Desktop\\CryptoMate\\dataset\\Cryptocurrency_Dataset_2023.csv")

df["Price (Intraday)"] = df["Price (Intraday)"].str.replace(",", "").astype(float)

df["Market Cap"] = df["Market Cap"].replace('[^\d.]', '', regex=True).astype(float)

percent_columns = ["% Change"]
for col in percent_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df.dropna(inplace=True)

symbols = list(df["Symbol"].unique())
names = list(df["Name"].unique())

layout = {"margin": {"l": 220}}

symbol = []
name = []

page = """
<|toggle|theme|>

<|25 75|layout|gap=30px|
<|sidebar|
## **Filter here 👻👩🏻‍💻 **{: style="color: #D875C7"}

<|{symbol}|selector|lov={symbols}|multiple|label=Select the Symbol|dropdown|on_change=on_filter|class_name=fullwidth|>

<|{name}|selector|lov={names}|multiple|label=Select the Name|dropdown|on_change=on_filter|class_name=fullwidth|>

|>

<main_page|
# 📊 **Cryptocurrency Dashboard**{: style="color: #B7C9F2"}

<|1 1 1|layout|
<total_market_cap|
## **Total Market Cap**{: style="color: #D875C7"}
US $ <|{int(df_selection["Market Cap"].sum())}|>
|total_market_cap>

<average_price|
## **Average Price (Intraday)**{: style="color: #D875C7"}
US $ <|{round(df_selection["Price (Intraday)"].mean(), 2)}|>
|average_price>

<average_change|
## **Average Change**{: style="color: #D875C7"}
<|{round(df_selection["Change"].mean(), 2)}|>%
|average_change>
|>

<br/>

<|Crypto Table|expandable|not expanded|
<|{df_selection}|table|page_size=5|>
|>

<|Crypto Plots|expandable|not expanded|


<|Line Graph|
### **InSights ☆°•°☆**{: style="color: #ff00ff"}
<|{x_selected}|selector|lov={numeric_columns}|dropdown=True|label=Select X Axis|>

<|{y_selected}|selector|lov={numeric_columns}|dropdown=True|label=Select Y Axis|>

<|{df_selection}|chart|type=line|properties={properties_line_graph}|rebuild|x={x_selected}|y={y_selected}|height=600px|>
|>
### **Pie Chart Visualisation ☆°•°☆**{: style="color: #ff00ff"}
<|{df_selection}|chart|type=pie|values=Market Cap|labels=Symbol|>

|>

|main_page>
|>

"""

def filter(symbol, name):
    df_selection = df[
        df["Symbol"].isin(symbol)
        & df["Name"].isin(name)
    ]

    print("Number of rows after filtering:", len(df_selection)) 

    return df_selection

def on_filter(state):
    if len(state.symbol) == 0 or len(state.name) == 0:
        notify(state, "Error", "Ok Ok !! processsing select name also 🤯")
        return
    
    state.df_selection = filter(
        state.symbol, state.name
    )


x_selected = "Price (Intraday)"
y_selected = "Change"
numeric_columns = ["Price (Intraday)", "Change", "% Change", "Market Cap", "Volume in Currency (Since 0:00 UTC)", "Volume in Currency (24Hr)", "Total Volume All Currencies (24Hr)", "Circulating Supply"]

about_page_content = """
# **About Me**{: style="color: #B7C9F2"}

<div style="display: flex; align-items: center; justify-content: space-around;border-radius: 2%; border: 3px solid #FFD1E3;margin-bottom:5px; position: relative;">
    <div style="flex: 1; text-align: center;">
        <img src="sneha.jpg" alt="Your Picture" style="border-radius: 50%; padding: 10px; border: 3px solid #D875C7; width: 300px; height: 280px; " />
        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; border-radius: 2%; box-shadow: 0 0 20px 10px #D875C7; pointer-events: none;"></div>
    </div>
    <div style="flex: 1; padding: 20px;">
        <p style="font-size: 18px; color: #7BC9FF;">Hi there! 👋 I'm Sneha, the creator of this Crypto Dashboard. I'm passionate about cryptocurrencies and data analysis. This project aims to provide insights into cryptocurrency trends using Python and Taipy.</p>
        
        <h3 style="color: #D875C7; font-size: 24px; margin-top: 20px;">Features:</h3>
        <ul style="font-size: 18px; color: #7EA1FF;">
            <li><strong>Dynamic Filtering:</strong> Easily filter cryptocurrencies by symbol and name to focus on specific assets.</li>
            <li><strong>Interactive Charts:</strong> Visualize cryptocurrency data with interactive line graphs and pie charts.</li>
            <li><strong>Real-time Updates:</strong> Get instant updates on total market capitalization, average prices, and changes.</li>
            <li><strong>User-friendly Interface:</strong> Enjoy a sleek and intuitive interface designed for seamless navigation.</li>
        </ul>
        
        <p style="font-size: 18px; color: #7BC9FF;">Feel free to explore the dashboard and reach out to me if you have any questions or feedback!</p>
    </div>
</div>
"""



if __name__ == "__main__":
    df_selection = filter(symbol, name)  
    total_market_cap = int(df_selection["Market Cap"].sum())
    page = page.replace("<|{int(df_selection['Market Cap'].sum())}|>", f"<|{total_market_cap}|>")
    
    pages = {
        "/": page,  # Main dashboard page
        "about": about_page_content  # About Me page
    }

    # Run the Taipy web server with the defined pages
    Gui(pages=pages).run(
        title="Crypto Dashboard",  # Set the title of the web application
        use_reloader=True  # Enable auto-reloading when source files are modified
    )

