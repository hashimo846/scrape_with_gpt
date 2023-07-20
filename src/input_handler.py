from google.oauth2 import service_account
import json
import os
from typing import Dict, List

INPUT_PATH = os.getenv('INPUT_PATH')
GOOGLE_CREDENTIAL_PATH = os.getenv('GOOGLE_CREDENTIAL_PATH')

def read_json(file_path:str) -> Dict:
    with open(file_path, 'r') as f:
        return json.load(f)

def get_master(master_url:str) -> Dict:
    pass

def main():
    credentials = service_account.Credentials.from_service_account_file(GOOGLE_CREDENTIAL_PATH)
    print(credentials)
    print(read_json(INPUT_PATH))

if __name__ == '__main__':
    main()
