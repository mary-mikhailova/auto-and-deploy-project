import string
import random
import configparser
import os
import pandas as pd
import re
from datetime import datetime, timedelta

dirname = os.path.dirname(__file__)

config = configparser.ConfigParser()
config.read(os.path.join(dirname, "config.ini"))

ITEMS_BY_CATEGORY = eval(config['Items_by_categoty']['ITEMS_BY_CATEGORY'])
DATA_FOLDER = config['Files']['DATA_FOLDER']

dirname_data = os.path.join(dirname, DATA_FOLDER)

if not os.path.exists(dirname_data):
    os.makedirs(dirname_data)

def generate_doc_id(length=20):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

def generate_date_time():
    today = datetime.today()
    start = datetime(today.year, today.month, today.day, 0, 0, 0)
    end = start + timedelta(days=1)-timedelta(seconds=1)
    random_seconds = random.randint(0, int((end-start).total_seconds()))
    random_time = start + timedelta(seconds=random_seconds)
    return random_time


def generate_csv_files(shop=4, cash=5):
    
    #если уже сущесвуют данные за предыдущий день, зачищаем их
    pattern = r"\d+_\d+\.csv"
    for file_name in os.listdir(dirname_data):
        if re.match(pattern, file_name):
            file_path=os.path.join(dirname_data, file_name)
            os.remove(file_path)

    for shop_num in range(1, shop+1):
        for cash_num in range (1, random.randint(2, cash+1)):
            filename = f'{shop_num}_{cash_num}.csv'
            data = []
            #количество чеков
            for _ in range(1, random.randint(6, 14)):
                shop_num = shop_num
                cash_num=cash_num
                doc_id = generate_doc_id()

                #генерация времени старта покупки (пробития чека)
                base_time = generate_date_time()

                #количество товаров(строк) на чек
                for line_num in range(1, random.randint(1, 5)):
                    #если в чеке будет несколько позиций, предположим, что они пробиваются с интервалом в 2 секунды
                    dt = (base_time + timedelta(seconds=2 * line_num)).strftime('%Y-%m-%d %H:%M:%S')

                    #категрия и тип товара выбираются из усталонвленного в сети магазинов ассортимента (в конфиге)
                    category = random.choice(list(ITEMS_BY_CATEGORY.keys()))
                    item = random.choice(list(ITEMS_BY_CATEGORY[category]))
                    
                    amount = random.randint(1,10)

                    #у каждого продукта генерируется цена из установленной ценовой категории
                    if category == 'бытовая химия':
                        price = round(random.uniform(100, 500),2)
                    elif category == 'текстиль':
                        price = round(random.uniform(400, 4000),2)
                    elif category == 'посуда':
                        price = round(random.uniform(300, 2000),2)
                    elif category == 'фрукты и овощи':
                        price = round(random.uniform(50, 300),2)
                    elif category == 'молоко и молочные продукты':
                        price = round(random.uniform(70, 250),2)
                    elif category == 'напитки и соки':
                        price = round(random.uniform(100, 300),2)

                    #генерация скидки с предположением, что она не может быть больше 30% от стоимости единицы товара
                    discount = round(random.uniform(0.00, price*0.3),2)

                    data.append([dt, shop_num, cash_num, doc_id, item, category, amount, price, discount])

            columns = ['dt', 'shop_num', 'cash_num', 'doc_id', 'item', 'category', 'amount', 'price', 'discount']

            df=pd.DataFrame(data, columns=columns)

            df.to_csv(os.path.join(dirname, "data", filename),index=False)

generate_csv_files()
