import json
import os

def read_json(file_path='data/input.json'):
    with open(file_path, 'r') as f:
        return json.load(f)

def main():
    print(read_json())
    # print(os.getcwd())

if __name__ == '__main__':
    main()
