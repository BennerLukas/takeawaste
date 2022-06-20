import pandas as pd
from fbprophet import Prophet

data = pd.read_csv("restaurant-1-orders.csv")

#slect only needed columns
data_port = data[["Order Date", "Product Price", "Quantity", "Total products"]]

# drop NaN-Cases
data_port = data_port.dropna()


#change to datetime
data_port["Order Date"] = pd.to_datetime(data_port["Order Date"])


data_ts = data_port[["Order Date", "Total products"]]

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
'DATABASE=teefabrik;'
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
    command='insert into teebeutel (datum,maschine,sorte) values (current_timestamp(),"'+machineID+'","Earl Grey");'
    #print(command)
    execute(command)

#inserts a temperature-event to the table temperatur
def predict(machineID,temperature):
    command='insert into temperatur (datum,maschine,temperatur) values (current_timestamp(),"'+machineID+'",'+str(temperature)+');'
    #print(command)
    execute(command)
