import pandas as pd
from fbprophet import Prophet
import numpy as np
import pyodbc



def forecasting():
    restaurant_id = input('geben sie eine RestaurantID an:')
    name_csv = str(input('geben sie den Namen der Zieldatei an: (z.B. restaurant.csv)'))
    column_date = str(input('Name der Spalte mit dem Datum:'))
    column_product_name = str(input('Name der Spalte mit den Produktnamen:'))
    column_quantity = str(input('Name der Spalte mit der Quantity:'))
    column_sold_products = str(input('Name der Spalte mit der Anzahl der verkauften Produkte:'))
    data = pd.read_csv(name_csv)

    data_ts = data[[column_date, column_product_name, column_quantity, column_sold_products]]
    data_ts = data_ts.dropna()

    #change to datetime
    data_ts[column_date] = pd.to_datetime(data_ts[column_date])
    data_ts[column_date] = pd.to_datetime(data_ts[column_date], format='%Y%m%d')



    data_grouped = data_ts.groupby([column_product_name])[column_sold_products, column_quantity].sum()
    #data_grouped.tail(100)

    # get the top 10 most sold products
    top_ten = data_grouped.sort_values(by = str(column_sold_products), ascending=False).head(10)
    top_ten_list = top_ten.index.tolist()


    # connect to Database
    connection_string = (
    'DRIVER=MySQL ODBC 8.0 ANSI Driver;'
    'SERVER=localhost;'
    'DATABASE=restaurant_products;'
    'UID=root;'
    'PWD=;'
    'charset=utf8mb4;'
    )

    conn=pyodbc.connect(connection_string)

    def execute(command):
            cursor=conn.cursor()
            cursor.execute(command)
            cursor.commit()



        #inserts the forecasting into the database
    def predict(restaurantID, date, quantity, min_quantity, max_quantity, item):
        command='insert into prediction (restaurantId,datum,quantity,max_quantity,min_quantity, product_name) values ("'+str(restaurantID)+'", "'+str(date)+'",'+str(quantity)+','+str(min_quantity)+','+str(max_quantity)+',"'+str(item)+'");'
        #print(command)
        execute(command)

    for item in top_ten_list:
        is_item = data_ts[column_product_name]==item
        data_item = data_ts[is_item]
        data_item[column_date] = pd.to_datetime(data_item[column_date].dt.strftime('%Y-%m-%d'))
        data_item_grouped = data_item.groupby([column_date])[column_sold_products].sum()
        date = data_item_grouped.index.tolist()
        df_data_item_grouped = data_item_grouped.to_frame()
        #print(date)
        df_data_item_grouped['Datum'] = date
        #data_item_grouped['Order Date'] = data_item_grouped.index
        df_data_item_grouped.reset_index(drop=True, inplace=True)



        df_data_item_grouped.rename(columns= {'Datum':'ds', column_sold_products:'y'}, inplace = True)
        list = df_data_item_grouped['y']
        df_data_item_grouped.pop('y')
        df_data_item_grouped['y'] = list


        m = Prophet()
        m.fit(df_data_item_grouped)


        future_week = m.make_future_dataframe(periods=7)
        future_week.tail(7) 


        forecast_week = m.predict(future_week)

        print(forecast_week[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(7))

        prediction_seven_days_df = forecast_week[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(7)

        for index, rows in prediction_seven_days_df.iterrows():

            date = rows['ds']
            quantity = rows['yhat']
            min_quantity = rows['yhat_lower']
            max_quantity = rows['yhat_upper']



            predict(restaurant_id, date, quantity, min_quantity, max_quantity, item)

forecasting()
