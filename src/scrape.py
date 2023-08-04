from bs4 import BeautifulSoup
from logging import DEBUG, INFO
import requests
from src import log
from time import sleep
from typing import List

# ロガーの初期化
logger = log.init(__name__, DEBUG)

# 商品ページから全テキストを取得 (ページからテキストを抽出できない場合はinput_textを入力)
def scrape_all_text(url:str = None, input_text:str = None) -> str:
    # ページから文字列を抽出 or 引数から文字列を抽出
    if input_text == None:
        # URLからページを取得
        logger.info(log.format('URLからテキストを取得中'))        
        while True:
            try:
                with requests.get(url, timeout=(3.0, 7.5)) as r:
                    html = BeautifulSoup(r.content, 'html.parser')
                    text = html.text
            except Exception as e:
                logger.error(log.format('アクセス失敗',e))
                sleep(1)
                logger.info(log.format('URLからテキストを再取得中'))
                continue
            else:
                break
    else:
        text = input_text
    # テキストのみ抽出
    text = text.replace(' ', '').replace('　', '').replace('\n', '').replace('\t', '')
    text = text.replace('\r', '').replace('\v', '').replace('\f', '')
    return text