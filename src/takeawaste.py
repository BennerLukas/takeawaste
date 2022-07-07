from database import Connector
from utils import set_logger
import pandas as pd
import os
from fbprophet import Prophet
import json

log = set_logger("TakeAWaste", mode="debug")


class TakeAWaste:

    def __init__(self):
        self.restaurant_id = None
        self.name_csv = None
        self.column_date = None
        self.column_product_name = None
        self.column_quantity = None
        self.column_sold_products = None

        self.data_path = "../data"
        self.raw_data = None
        self.prepped_data = None

        self.log = log
        self.db = Connector(log)

        pass

    def set_params_by_json(self, filename="metadata.json"):
        f = open(os.path.join(self.data_path, filename))
        params = json.load(f)
        self.log.debug(params)
        value_list = list(params.values())

        if len(value_list) != 6:
            self.log.error("Wrong number of params in metadata.json")
            raise

        self.restaurant_id = value_list[0]
        self.name_csv = value_list[1]
        self.column_date = value_list[2]
        self.column_product_name = value_list[3]
        self.column_quantity = value_list[4]
        self.column_sold_products = value_list[5]

    def set_params_manually(self):
        self.restaurant_id = input('geben sie eine RestaurantID an:')
        self.name_csv = str(input('geben sie den Namen der Zieldatei an: (z.B. restaurant.csv)'))
        self.column_date = str(input('Name der Spalte mit dem Datum:'))
        self.column_product_name = str(input('Name der Spalte mit den Produktnamen:'))
        self.column_quantity = str(input('Name der Spalte mit der Quantity:'))
        self.column_sold_products = str(input('Name der Spalte mit der Anzahl der verkauften Produkte:'))

    def read_data(self):
        full_path = os.path.join(self.data_path, self.name_csv)
        self.log.debug(f"Read data from {full_path}")
        self.raw_data = pd.read_csv(full_path)

    def prep_data(self, n_limit=10):
        self.log.debug("Prepare Data")
        self.prepped_data = self.raw_data[
            [self.column_date, self.column_product_name, self.column_quantity, self.column_sold_products]]
        self.prepped_data = self.prepped_data.dropna()

        # change to datetime
        self.prepped_data[self.column_date] = pd.to_datetime(self.prepped_data[self.column_date])
        self.prepped_data[self.column_date] = pd.to_datetime(self.prepped_data[self.column_date], format='%Y%m%d')

        data_grouped = self.prepped_data.groupby([self.column_product_name])[
            self.column_sold_products, self.column_quantity].sum()

        # get the top 10 most sold products
        top_n = data_grouped.sort_values(by=str(self.column_sold_products), ascending=False).head(n_limit)
        top_n_list = top_n.index.tolist()

        return top_n_list

    def forcasting(self, top_n_list):
        self.log.debug("Start Forecasting")
        for item in top_n_list:
            is_item = self.prepped_data[self.column_product_name] == item
            data_item = self.prepped_data[is_item]
            data_item[self.column_date] = pd.to_datetime(data_item[self.column_date].dt.strftime('%Y-%m-%d'))
            data_item_grouped = data_item.groupby([self.column_date])[self.column_sold_products].sum()
            date = data_item_grouped.index.tolist()
            df_data_item_grouped = data_item_grouped.to_frame()
            # print(date)
            df_data_item_grouped['Datum'] = date
            # data_item_grouped['Order Date'] = data_item_grouped.index
            df_data_item_grouped.reset_index(drop=True, inplace=True)

            df_data_item_grouped.rename(columns={'Datum': 'ds', self.column_sold_products: 'y'}, inplace=True)

            # reorder col order
            col_y = df_data_item_grouped['y']
            df_data_item_grouped.pop('y')
            df_data_item_grouped['y'] = col_y

            m = Prophet()
            m.fit(df_data_item_grouped)

            future_week = m.make_future_dataframe(periods=7)
            future_week.tail(7)

            forecast_week = m.predict(future_week)

            self.log.debug(forecast_week[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(7))

            prediction_seven_days_df = forecast_week[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(7)

            return prediction_seven_days_df

    def execute(self):
        self.read_data()
        top_list = self.prep_data()
        df_forecast = self.forcasting(top_list)
        self.db.insert_df2db(df_forecast)


if __name__ == "__main__":
    obj = TakeAWaste()
    obj.set_params_by_json()
    obj.execute()
    pass
