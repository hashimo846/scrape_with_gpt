from google.oauth2 import service_account
import google.auth.exceptions
import gspread
import json
import os
from time import sleep
from typing import Dict, List, Tuple

# constant
INPUT_PATH = os.getenv('INPUT_PATH')
GOOGLE_CREDENTIAL_PATH = os.getenv('GOOGLE_CREDENTIAL_PATH')
MASTER_WORKSHEET = '項目_詳細情報'
PRODUCT_WORKSHHET = '商品_詳細情報'

# read json file with path
def read_json(file_path:str) -> Dict:
    with open(file_path, 'r') as f:
        return json.load(f)

# autorize google spreadheet and google drive api
def authorize_gspread(credential_path:str = GOOGLE_CREDENTIAL_PATH) -> gspread.Client:
    credentials =  service_account.Credentials.from_service_account_file(
        credential_path, 
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive',
        ]
    )
    gspread_client = gspread.authorize(credentials)
    return gspread_client

# get spreadsheet with url
def get_spreadsheet(sheet_url:str) -> gspread.Spreadsheet:
    gspread_client = authorize_gspread()
    spreadsheet = gspread_client.open_by_url(sheet_url)
    return spreadsheet

# get all values from worksheet in spreadsheet
def get_table(sheet_url:str, worksheet_name:str) -> List:
    while True:
        try:
            spreadsheet = get_spreadsheet(sheet_url)
            worksheet = spreadsheet.worksheet(worksheet_name)
            table = worksheet.get_all_values()
        except google.auth.exceptions.TransportError as e:
            print('#Error: [{}]{}'.format(type(e),e))
            sleep(1)
            print('#Retry: スプレッドシートからテーブル再取得中', end='...')
            continue
        else:
            break
    return table

def get_column(table:List, idx:int) -> List:
    return [row[idx] for row in table]

# get master data from spreadsheet with url
def get_master(sheet_url:str) -> Dict:
    # get master table
    print('#Log: スプレッドシートからマスタ情報取得中', end='...')
    master_table = get_table(sheet_url, MASTER_WORKSHEET)
    print('完了')
    # get each column
    master = {
        'features': get_column(master_table, 0),
        'descriptions': get_column(master_table, 1),
        'formats': get_column(master_table, 2),
        'units': get_column(master_table, 3),
        'filters': get_column(master_table, 4),
    }
    return master

# get boolean items from master data
def get_boolean_items(master:Dict) -> List:
    items, i = [], 0
    while i < len(master['formats']):
        if master['formats'][i] == '二値':
            items.append(master['features'][i])
        i += 1
    return items

# get data items from master data
def get_data_items(master:Dict) -> List:
    items, i = [], 0
    while i < len(master['formats']):
        if master['formats'][i] in ['小数','整数','フリーワード']:
            name = master['features'][i]
            value_type = master['formats'][i]
            unit = master['units'][i] if master['units'][i] != '' else None
            items.append({'name':name, 'value_type':value_type, 'unit':unit})
        i += 1
    return items

# get option items from master data
def get_option_items(master:Dict) -> List:
    items, i = [], 0
    while i < len(master['formats']):
        if master['formats'][i] == '管理用の値':
            name = master['features'][i]
            options = [master['filters'][i]]
            i += 1
            while i < len(master['formats']) and master['features'][i] == '':
                options.append(master['filters'][i])
                i += 1
            items.append({'name':name, 'options':options})
        else:
            i += 1
    return items

# get all items from master
def get_all_items() -> Dict:
    # read input from json
    input_data = read_json(INPUT_PATH)
    # get master data from spreadsheet
    master = get_master(input_data['sheet_url'])
    # get each items
    boolean_items = get_boolean_items(master)
    data_items = get_data_items(master)
    option_items = get_option_items(master)
    # to dict
    items = {
        'boolean_items':boolean_items, 
        'data_items':data_items,
        'option_items':option_items,
    }
    return items

# extract valid columns from product table
def extract_valid_columns(target_row:List) -> Dict:
    important_keys = {'JAN(変更不可)':'jan', '商品ID(変更不可)':'id', 'メーカー名(変更不可)':'maker', '商品名(変更不可)':'name', '参照URL(編集可能)':'reference_url', '入力文(任意)':'input_text'}
    valid_columns = {}
    for idx, value in enumerate(target_row):
        if value.split(':')[-1] == '表示用':
            continue
        elif value.split(':')[-1] == '管理用':
            key = ''.join(value.split(':')[:-1])
        elif value in important_keys:
            key = important_keys[value]
        # valid_columns = {key:idx}
        valid_columns[key] = idx
    return valid_columns

# extract product from target_row. if jan is not found, return None
def extract_product(valid_columns:Dict, target_row:List) -> Dict:
    product = dict()
    for key in valid_columns.keys():
        product[key] = target_row[valid_columns[key]]
    if product['jan'] == '':
        return None
    else:
        return product

# get all products from product sheet
def get_all_products() -> List:
    # read input from json
    input_data = read_json(INPUT_PATH)
    # get all data of product sheet
    print('#Log: スプレッドシートから商品情報取得中', end='...')
    product_table = get_table(input_data['sheet_url'], PRODUCT_WORKSHHET)
    print('完了')

    # extract valid columns
    valid_columns = extract_valid_columns(product_table[0])
    # get products list
    products = []
    for target_row in product_table[1:]:
        product = extract_product(valid_columns, target_row)
        if product is not None:
            products.append(product)
    return products

def print_log(title:str, content:any) -> None:
    print('\n======= {} ======='.format(title))
    print(content)

def main():
    items = get_all_items()
    print_log('boolean_items', items['boolean_items'])
    print_log('data_items',items['data_items'])
    print_log('option_items', items['option_items'])
    # get products
    products = get_all_products()
    print_log('products', products)

if __name__ == '__main__':
    main()