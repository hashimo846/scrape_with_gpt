from bs4 import BeautifulSoup
from langchain.text_splitter import TokenTextSplitter
import openai
import os
import requests
from typing import List, Dict

# 1プロンプトに含む入力のトークン数の上限
PROMPT_TOKEN_LIMIT = 3500
# 入力を分割する際の重複するトークン数
TOKEN_OVERLAP = 100

# プロンプトのテンプレート
def str_template(model_number:str, is_service = False):
    template = '今から与える入力のみを用いて、'
    if model_number != None: 
        template += '製品' + model_number + 'の'
    else:
        template += '商品の'
    template += '仕様や性能を示す情報を抽出してください。\n'
    template += 'ただし、定量的な数値情報や固有名詞は可能は限り出力に含めてください。\n\n'
    template += '#入力\n{}'
    return template

# 入力を決められたトークン数ごとに分割する
def split_by_token(input_text, prompt_token_limit = PROMPT_TOKEN_LIMIT, token_overlap = TOKEN_OVERLAP):
    text_splitter = TokenTextSplitter(chunk_size=prompt_token_limit, chunk_overlap=token_overlap)
    texts = text_splitter.split_text(input_text)
    return texts

# OpenAI APIの認証
def authentication_openai():
    openai.organization = os.getenv("OPENAI_ORGANIZATION")
    openai.api_key = os.getenv("OPENAI_API_KEY")

# プロンプトを送信して回答を取得
def send_prompt(prompt):
    # make messages
    messages = [{'role':'user', 'content':prompt}]
    # send prompt
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = messages
    )
    return response.choices[0]['message']['content'].strip()

# 商品ページからテキストを取得してGPTに入力し、商品情報をスクレイピング
def summarize(input_text:str, model_number:str = None) -> str:
    # 入力分が長い場合は複数に分割
    split_texts = split_by_token(input_text)
    # GPTに入力用のプロンプトを作成
    scrape_prompts = [str_template(model_number).format(text) for text in split_texts]
    # GPTの回答を取得
    authentication_openai()
    extract_texts = [send_prompt(prompt) for prompt in scrape_prompts]
    # 回答を結合
    extract_text = '\n'.join(extract_texts)
    return extract_text