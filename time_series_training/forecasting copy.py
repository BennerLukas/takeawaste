import pandas as pd
from fbprophet import Prophet
import numpy as np


data = pd.read_csv("restaurant-1-orders.csv")

#slect only needed columns
data_port = data[["Order Date","Item Name", "Product Price", "Quantity", "Total products"]]

# drop NaN-Cases
data_port = data_port.dropna()


#change to datetime
data_port["Order Date"] = pd.to_datetime(data_port["Order Date"])


data_ts = data_port[["Order Date","Item Name", "Total products"]]

#es soll eine schleife entstehen die jeweils ein Produkt aus dem Dataframe wählt und entsprechend für den Schleifendurchlauf einen DF
#der nur Einträge zu diesem Produkt besitzt 

# df (prod, date, price)

data_ts.rename(columns= {'Order Date':'ds', 'Total products':'y'}, inplace = True)

m = Prophet()
m.fit(data_ts)

future_week = m.make_future_dataframe(periods=7)

forecast_week = m.predict(future_week)


tail = forecast_week['yhat'].tail(7)


vorhersage = tail.tolist()


import pyodbc

connection_string = (
'DRIVER=MySQL ODBC 8.0 ANSI Driver;'
'SERVER=localhost;'
'DATABASE=restaurant_forecasting;'
'UID=root;'
'PWD=;'
'charset=utf8mb4;'
)

conn=pyodbc.connect(connection_string)

#executes an command like insert / create
def execute(command):
    cursor=conn.cursor()
    cursor.execute(command)
    cursor.commit()

#inserts an product to table teebeutel
def predict(machineID):
    command='insert into teebeutel (restaurantID,datum,,sorte) values (current_timestamp(),"'+machineID+'","Earl Grey");'
    #print(command)
    execute(command)

#inserts a temperature-event to the table temperatur
def predict(date, restaurantID, quantity, min_quantity, max_quantity):
    command='insert into restaurant_prediction (restaurantId,datum,quantity,max_quantity,min_quantity) values ("'+date+'","'+restaurantID+'",'+str(quantity)+','+str(min_quantity)+','+str(max_quantity)+');'
    #print(command)
    execute(command)




tail_df = forecast_week[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(7)

database_df = tail_df.reset_index(drop=True)

restaurantID = np.random.randint(20000000)

#Vorhersagen in Database speichern
for i in range(0, 7):
    date = database_df['ds'].iloc[i]
    quantity = database_df['yhat'].iloc[i]
    min_quantity = database_df['yhat_lower'].iloc[i]
    max_quantity = database_df['yhat_upper'].iloc[i]


    predict(date, restaurantID, quantity, min_quantity, max_quantity)