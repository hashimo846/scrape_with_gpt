from bs4 import BeautifulSoup
import requests
from typing import List

# 商品ページから全テキストを取得 (ページからテキストを抽出できない場合はinput_textを入力)
def scrape_all_text(url:str = None, input_text:str = None) -> str:
    # ページから文字列を抽出 or 引数から文字列を抽出
    if input_text == None:
        # URLからページを取得
        with requests.get(url) as r:
            html = BeautifulSoup(r.content, 'html.parser')
            text = html.text
    else:
        text = input_text
    # テキストのみ抽出
    text = text.replace(' ', '').replace('　', '').replace('\n', '').replace('\t', '')
    text = text.replace('\r', '').replace('\v', '').replace('\f', '')
    return text