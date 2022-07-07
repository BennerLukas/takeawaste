import pyodbc
import sqlalchemy
import pymysql

class Connector:
    def __init__(self):
        # connect to Database
        connection_string = (
            'DRIVER=MySQL ODBC 8.0 ANSI Driver;'
            'SERVER=localhost;'
            'DATABASE=takeawaste;'
            'UID=root;'
            'PWD=1234;'
            'charset=utf8mb4;'
        )
        self.conn = pyodbc.connect(connection_string)
        alchemy_engine = sqlalchemy.create_engine(
            f'mysql+pymysql://root:1234@localhost:3306/takeawaste')
        self.alchemy_conn = alchemy_engine.connect()

    def execute(self, command):
        cursor = self.conn.cursor()
        cursor.execute(command)
        cursor.commit()

    def insert_df2db(self, df, table_name="Prediction"):
        df.to_sql(table_name, self.db.alchemy_conn, if_exists="append")
        return True
