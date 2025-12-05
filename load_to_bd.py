import os
import configparser
import re
import pandas as pd

from pgdb import PGDatabase

dirname = os.path.dirname(__file__)

config = configparser.ConfigParser()
config.read(os.path.join(dirname, "config.ini"))

DATA_FOLDER = config['Files']['DATA_FOLDER']
DATABASE_CREDS = config['Database']

dirname_data = os.path.join(dirname, DATA_FOLDER)


database = PGDatabase(
    host=DATABASE_CREDS['HOST'],
    port=DATABASE_CREDS['PORT'],
    database=DATABASE_CREDS['DATABASE'],
    user=DATABASE_CREDS['USER'],
    password=DATABASE_CREDS['PASSWORD']
)

sales_df = pd.DataFrame()
if os.path.exists(dirname_data):
    pattern = r"\d+_\d+\.csv"
    for file_name in os.listdir(dirname_data):
        if re.match(pattern, file_name):
            file_path=os.path.join(dirname_data, file_name)
            sales_df=pd.read_csv(file_path)
            for i, row in sales_df.iterrows():
                query = f"""
                INSERT INTO sales_shop_cash (dt, shop_num, cash_num, doc_id, item, category, amount, price, discount)
                VALUES ('{row['dt']}', {row['shop_num']}, {row['cash_num']}, '{row['doc_id']}', 
                '{row['item']}', '{row['category']}', {row['amount']}, {row['price']}, {row['discount']})
                """
                database.post(query)

