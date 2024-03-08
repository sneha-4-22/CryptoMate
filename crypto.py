import pandas as pd
from taipy.gui import Gui, notify
import numpy as np
df = pd.read_csv("C:\\Users\\Sneha\\Desktop\\FitMate\\dataset\\Cryptocurrency_Dataset_2023.csv")

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
## **Filter here ☆ **{: style="color: #ff1493"}

<|{symbol}|selector|lov={symbols}|multiple|label=Select the Symbol|dropdown|on_change=on_filter|class_name=fullwidth|>

<|{name}|selector|lov={names}|multiple|label=Select the Name|dropdown|on_change=on_filter|class_name=fullwidth|>

|>

<main_page|
# 📊 **Cryptocurrency Dashboard**{: style="color: #c52222"}

<|1 1 1|layout|
<total_market_cap|
## **Total Market Cap**{: style="color: #ff1493"}
US $ <|{int(df_selection["Market Cap"].sum())}|>
|total_market_cap>

<average_price|
## **Average Price (Intraday)**{: style="color: #ff1493"}
US $ <|{round(df_selection["Price (Intraday)"].mean(), 2)}|>
|average_price>

<average_change|
## **Average Change**{: style="color: #ff1493"}
<|{round(df_selection["Change"].mean(), 2)}|>%
|average_change>
|>

<br/>

<|Crypto Table|expandable|not expanded|
<|{df_selection}|table|page_size=5|>
|>

<|Crypto Plots|expandable|not expanded|


<|Line Graph|
### InSights ☆°•°☆
<|{x_selected}|selector|lov={numeric_columns}|dropdown=True|label=Select X Axis|>

<|{y_selected}|selector|lov={numeric_columns}|dropdown=True|label=Select Y Axis|>

<|{scatter_dataset}|chart|type=line|properties={properties_line_graph}|rebuild|x={x_selected}|y={y_selected}|height=600px|>
|>

<|Scatter|
### Scatter
<|layout|columns= 1 2|
<|{x_selected}|selector|lov={numeric_columns}|dropdown|label=Select X Axis|>

<|{y_selected}|selector|lov={numeric_columns}|dropdown|label=Select Y Axis|>
|>

<|{scatter_dataset}|chart|properties={properties_scatter_dataset}|rebuild|color[1]=red|color[2]=green|name[1]=Exited|name[2]=Stayed|mode=markers|type=scatter|height=600px|>
|>
|>

<|Crypto Table|expandable|not expanded|
<|{df_selection}|table|page_size=5|>
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
        notify(state, "Error", "No results found. Check the filters.")
        return
    
    state.df_selection = filter(
        state.symbol, state.name
    )
def creation_scatter_dataset(test_dataset:pd.DataFrame):
    scatter_dataset = test_dataset.copy()

    for column in scatter_dataset.columns:
        if column != 'EXITED' :
            column_neg = str(column)+'_neg'
            column_pos = str(column)+'_pos'
            
            scatter_dataset[column_neg] = scatter_dataset[column]
            scatter_dataset[column_pos] = scatter_dataset[column]
            
            scatter_dataset.loc[(scatter_dataset['EXITED'] == 1),column_neg] = np.NaN
            scatter_dataset.loc[(scatter_dataset['EXITED'] == 0),column_pos] = np.NaN
    
    return scatter_dataset


x_selected = "Price (Intraday)"
y_selected = "Change"
numeric_columns = ["Price (Intraday)", "Change", "% Change", "Market Cap", "Volume in Currency (Since 0:00 UTC)", "Volume in Currency (24Hr)", "Total Volume All Currencies (24Hr)", "Circulating Supply"]

scatter_dataset = df.copy()  
properties_scatter_dataset = {"x": x_selected, "y[1]": y_selected + '_pos', "y[2]": y_selected + '_neg'}


def update_histogram_and_scatter(state):
    global x_selected, y_selected, scatter_dataset, histo_full
    x_selected = state.x_selected
    y_selected = state.y_selected
    state.properties_line_graph = {"x": x_selected, "y": y_selected}
    state.scatter_dataset = scatter_dataset
    state.scatter_dataset_pred = scatter_dataset

   
if __name__ == "__main__":
    df_selection = filter(symbol, name)  
    total_market_cap = int(df_selection["Market Cap"].sum())
    page = page.replace("<|{int(df_selection['Market Cap'].sum())}|>", f"<|{total_market_cap}|>")
    
    Gui(page).run(margin="0em", title="Crypto Dashboard")
