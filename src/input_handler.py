import json
from google.oauth2.service_account import Credentials
import gspread
from typing import Dict, List

def read_json(file_path:str='data/input.json') -> Dict:
    with open(file_path, 'r') as f:
        return json.load(f)

def get_master(master_url:str) -> Dict:
    pass

def main():
    print(read_json())

if __name__ == '__main__':
    main()
