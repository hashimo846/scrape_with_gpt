from google.oauth2 import service_account
import gspread
import json
import os
from typing import Dict, List, Tuple

# constant
INPUT_PATH = os.getenv('INPUT_PATH')
GOOGLE_CREDENTIAL_PATH = os.getenv('GOOGLE_CREDENTIAL_PATH')

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

# get master data from spreadsheet with url
def get_master(master_url:str) -> Dict:
    # get master sheet
    spreadsheet = get_spreadsheet(master_url)
    master_sheet = spreadsheet.worksheet('項目_詳細情報')
    # get each column
    master = {
        'features': [],
        'descriptions': [],
        'formats': [],
        'units': [],
        'filters': [],
    }
    max_row = 0
    for idx, key in enumerate(master):
        master[key] = master_sheet.col_values(idx+1)[1:]
        max_row = max(max_row, len(master[key]))
    # padding empty cells
    for idx, key in enumerate(master):
        while len(master[key]) < max_row:
            master[key].append('')
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
    while True:
        try:
            master = get_master(input_data['master_url'])
        except google.auth.exceptions.TransportError as e:
            print('Error: [{}}]{}'.format(type(e),e))
            sleep(5)
            print('Retry: get master data from spreadsheet')
            continue
        else:
            print('Success: get master data from spreadsheet')
            break
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

# get product info from input json
def get_product_info() -> Tuple[str, str, str]:
    # read input from json
    input_data = read_json(INPUT_PATH)
    product_url = input_data['product_url']
    model_number = input_data['model_number'] if input_data['model_number'] != '' else None
    input_text = input_data['input_text'] if input_data['input_text'] != '' else None
    return product_url, model_number, input_text

def main():
    # read input from json
    input_data = read_json(INPUT_PATH)
    # get master data from spreadsheet
    master = get_master(input_data['master_url'])
    # get each items
    boolean_items = get_boolean_items(master)
    data_items = get_data_items(master)
    option_items = get_option_items(master)
    print(boolean_items)
    print('=====')
    print(data_items)
    print('=====')
    print(option_items)
    print('=====')
    print()

if __name__ == '__main__':
    main()
