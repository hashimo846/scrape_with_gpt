from google.oauth2 import service_account
import google.auth.exceptions
import gspread
import json
from logging import DEBUG, INFO
import os
from src import log
from time import sleep
from typing import Dict, List, Tuple

# ロガーの初期化
logger = log.init(__name__, DEBUG)

# パラメータ
INPUT_PATH = os.getenv('INPUT_PATH')
GOOGLE_CREDENTIAL_PATH = os.getenv('GOOGLE_CREDENTIAL_PATH')
MASTER_WORKSHEET = '項目_詳細情報'
PRODUCT_WORKSHHET = '商品_詳細情報'

# Jsonファイルの読み込み
def read_json(file_path:str = INPUT_PATH) -> Dict:
    with open(file_path, 'r') as f:
        return json.load(f)

# Google APIの認証
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

# URLからスプレッドシートを取得
def get_spreadsheet(sheet_url:str) -> gspread.Spreadsheet:
    gspread_client = authorize_gspread()
    spreadsheet = gspread_client.open_by_url(sheet_url)
    return spreadsheet

# URLとシート名からテーブルを取得（List）
def get_table(sheet_url:str, worksheet_name:str) -> List:
    while True:
        try:
            spreadsheet = get_spreadsheet(sheet_url)
            worksheet = spreadsheet.worksheet(worksheet_name)
            table = worksheet.get_all_values()
        except google.auth.exceptions.TransportError as e:
            logger.error(log.format('スプレッドシート取得失敗', e))
            sleep(1)
            logger.info('スプレッドシートからテーブル再取得中')
            continue
        else:
            break
    return table

# 指定した列の全データをテーブルから取得
def get_column(table:List, idx:int) -> List:
    return [row[idx] for row in table]

# スプレッドシートのURLからマスタ情報を取得
def get_master(sheet_url:str) -> Dict:
    # get master table
    logger.info('スプレッドシートからマスタ情報取得中')
    master_table = get_table(sheet_url, MASTER_WORKSHEET)
    # get each column
    master = {
        'features': get_column(master_table, 0),
        'descriptions': get_column(master_table, 1),
        'formats': get_column(master_table, 2),
        'units': get_column(master_table, 3),
        'filters': get_column(master_table, 4),
    }
    return master

# マスタ情報から二値項目を取得
def get_boolean_items(master:Dict) -> List:
    items, i = [], 0
    while i < len(master['formats']):
        if master['formats'][i] == '二値':
            items.append(master['features'][i])
        i += 1
    return items

# マスタ情報からデータ項目を取得
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

# マスタ情報から選択項目を取得
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

# スプレッドシートからマスタ情報の全項目を取得
def get_master_items(sheet_url:str) -> Dict:
    # get master data from spreadsheet
    master = get_master(sheet_url)
    # get each items
    boolean_items = get_boolean_items(master)
    data_items = get_data_items(master)
    option_items = get_option_items(master)
    # to dict
    master_items = {
        'boolean':boolean_items, 
        'data':data_items,
        'option':option_items,
    }
    return master_items

# extract valid columns from product table
def extract_valid_columns(target_row:List) -> Dict:
    important_keys = {'JAN(変更不可)':'jan', 'メーカー名(変更不可)':'maker', '商品名(変更不可)':'name', '型番(変更不可)':'model_number', '参照URL(編集可能)':'reference_url', '実行ボタン':'execute_button'}
    valid_columns = {}
    for idx, value in enumerate(target_row):
        if value in important_keys:
            key = important_keys[value]
        elif value == '':
            continue
        else:
            key = (value)
        # valid_columns = {key:idx}
        valid_columns[key] = idx
    return valid_columns

def get_product_table(sheet_url:str) -> List:
    logger.info('スプレッドシートから商品情報取得中')
    product_table = get_table(sheet_url, PRODUCT_WORKSHHET)
    return product_table

# 商品情報を取得（janが空の場合はNoneを返す）
def get_product(sheet_url:str, target_row_idx:int) -> Dict:
    product_table = get_product_table(sheet_url)
    valid_columns = extract_valid_columns(product_table[0])
    target_row = product_table[target_row_idx]
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
    
    # extract valid columns
    valid_columns = extract_valid_columns(product_table[0])
    # get products list
    products = []
    for target_row in product_table[1:]:
        product = extract_product(valid_columns, target_row)
        if product is not None:
            products.append(product)
    return products, valid_columns

def output_data(product:Dict, valid_columns:Dict, data_answers:List) -> None:
    pass

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