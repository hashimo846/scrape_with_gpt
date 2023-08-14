from bs4 import BeautifulSoup
from logging import DEBUG, INFO
import requests
from src import log
from time import sleep
from typing import List

# ロガーの初期化
logger = log.init(__name__, DEBUG)

# HTTPリクエスト時のユーザーエージェント
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
header = {'User-Agent': user_agent}

# 商品ページから全テキストを取得 (ページからテキストを抽出できない場合はinput_textを入力)
def scrape_all_text(url:str = None, input_text:str = None) -> str:
    # ページから文字列を抽出 or 引数から文字列を抽出
    if input_text == None:
        # URLからページを取得
        logger.info(log.format('URLからテキストを取得中'))        
        try:
            with requests.get(url, headers = header, timeout=(3.0, 7.5)) as r:
                html = BeautifulSoup(r.content, 'html.parser')
                text = html.text
        except Exception as e:
            logger.error(log.format('アクセス失敗',e))
            return None
    else:
        text = input_text
    # テキストのみ抽出
    text = text.replace(' ', '').replace('　', '').replace('\n', '').replace('\t', '')
    text = text.replace('\r', '').replace('\v', '').replace('\f', '')
    return text

def main():
    url = 'https://store.acer.com/ja-jp/ap551-50w'
    text = scrape_all_text(url)
    print(text)

if __name__ == '__main__':
    main()