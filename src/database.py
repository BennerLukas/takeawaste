from pandas import DataFrame
import pyodbc
import sqlalchemy


class Connector:
    def __init__(self, log):
        self.log = log

        # connect to Database
        connection_string = (
            'DRIVER=MySQL ODBC 8.0 ANSI Driver;'
            'SERVER=localhost;'
            'DATABASE=;'
            'UID=root;'
            'PWD=1234;'
            'charset=utf8mb4;'
        )
        self.conn = pyodbc.connect(connection_string)

        self.executing("DROP DATABASE IF EXISTS takeawaste;")
        self.executing("Create DATABASE takeawaste;")

        alchemy_engine = sqlalchemy.create_engine(
            f'mysql+pymysql://root:1234@localhost:3306/takeawaste')
        self.alchemy_conn = alchemy_engine.connect()
        self.log.info("Connected to database")

    def executing(self, command):
        cursor = self.conn.cursor()
        cursor.execute(command)
        cursor.commit()

    def insert_df2db(self, df: DataFrame, table_name: str = "prediction") -> bool:
        """
        Insert a whole dataframe to the database
        :param df:
        :param table_name:
        :return:
        """
        self.log.info("Write df into database")
        df.to_sql(table_name, self.alchemy_conn, if_exists="append")
        return True
