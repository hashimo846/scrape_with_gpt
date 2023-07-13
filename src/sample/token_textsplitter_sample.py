import requests
from bs4 import BeautifulSoup
from langchain.document_loaders.image import UnstructuredImageLoader
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import TokenTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.chat_models import ChatOpenAI
import os

# 商品ページのURL
HTML_URL = 'https://www.katoji-onlineshop.com/c/category/babygate/63423'
# 型番
MODEL_NUMBER = ''
# 入力テキスト（API制限等によりスクレイピングできないときに入力）
INPUT_TEXT = ''

def scrape_all(url = HTML_URL, input_text = INPUT_TEXT):
    # URLからページを取得
    with requests.get(url) as r:
        html = BeautifulSoup(r.content, 'html.parser')
    # ページから文字列を抽出 or 引数から文字列を抽出
    if input_text == '':
        text = html.text
    else:
        text = input_text
    # テキストのみ抽出
    text = ''.join(text.split(' '))
    text = ''.join(text.split('　'))
    text = ''.join(text.split('\n'))
    text = ''.join(text.split('\t'))
    text = ''.join(text.split('\r'))
    text = ''.join(text.split('\v'))
    text = ''.join(text.split('\f'))
    return text

state_of_the_union = scrape_all()

text_splitter = TokenTextSplitter(chunk_size=3000, chunk_overlap=100)

texts = text_splitter.split_text(state_of_the_union)

for text in texts:
    print('###########')
    print(text)
    print('###########')