import pandas as pd
from taipy.gui import Gui, notify

df = pd.read_csv("C:\\Users\\Sneha\\Desktop\\FitMate\\dataset\\Cryptocurrency_Dataset_2023.csv")

df["Price (Intraday)"] = df["Price (Intraday)"].str.replace(",", "").astype(float)

percent_columns = ["% Change"]
for col in percent_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df.dropna(inplace=True)

symbol = symbols = list(df["Symbol"].unique())
name = names = list(df["Name"].unique())

layout = {"margin": {"l": 220}}



page = """
<|toggle|theme|>

<|25 75|layout|gap=30px|
<|sidebar|
## Please **filter**{: .color-primary} here:

<|{symbol}|selector|lov={symbols}|multiple|label=Select the Symbol|dropdown|on_change=on_filter|class_name=fullwidth|>

<|{name}|selector|lov={names}|multiple|label=Select the Name|dropdown|on_change=on_filter|class_name=fullwidth|>

|>

<main_page|
# 📊 Cryptocurrency **Dashboard**{: .color-primary}

<|1 1 1|layout|
<total_market_cap|
## **Total Market Cap**{: .color-primary}:
US $ <|{int(df_selection["Market Cap"].sum())}|>
|total_market_cap>

<average_price|
## Average **Price (Intraday)**{: .color-primary}:
US $ <|{round(df_selection["Price (Intraday)"].mean(), 2)}|>
|average_price>

<average_change|
## Average **Change**{: .color-primary}:
<|{round(df_selection["Change"].mean(), 2)}|>%
|average_change>
|>

<br/>

<|Crypto Table|expandable|not expanded|
<|{df_selection}|table|page_size=5|>
|>

Get the Taipy Code [here](https://github.com/Avaiga/demo-crypto-dashboard) 
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
        notify(state, "Error", "No results found. Check the filters.")
        return
    
    state.df_selection = filter(
        state.symbol, state.name
    )

if __name__ == "__main__":
    df_selection = filter(
        symbol, name
    )
    Gui(page).run(margin="0em", title="Crypto Dashboard")
