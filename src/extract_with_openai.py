import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import TokenTextSplitter
import openai
import os

# 商品ページのURL
HTML_URL = 'https://www.katoji-onlineshop.com/c/category/babygate/63423'
# 型番
MODEL_NUMBER = ''
# 入力テキスト（API制限等によりスクレイピングできないときに入力）
INPUT_TEXT = ''
# 1プロンプトに含む入力のトークン数の上限
PROMPT_TOKEN_LIMIT = 3500
# 入力を分割する際の重複するトークン数
TOKEN_OVERLAP = 100

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

# プロンプトのテンプレート
def str_template(model_number = MODEL_NUMBER, is_service = False):
    template = '今から与える入力のみを用いて、'
    if MODEL_NUMBER != '': 
        template += '製品' + model_number + 'の'
    else:
        template += '製品の'
    template += '詳細・性能を示す情報や、定量的な数値情報を抽出してください。\n\n'
    template += '#入力\n{}'
    return template

# 入力を決められたトークン数ごとに分割する
def split_input_text(input_text, prompt_token_limit = PROMPT_TOKEN_LIMIT, token_overlap = TOKEN_OVERLAP):
    text_splitter = TokenTextSplitter(chunk_size=prompt_token_limit, chunk_overlap=token_overlap)
    texts = text_splitter.split_text(input_text)
    return texts

# authentication openai api
def authentication_openai():
    openai.organization = os.getenv("OPENAI_ORGANIZATION")
    openai.api_key = os.getenv("OPENAI_API_KEY")

# send prompt
def send_prompt(prompt):
    # make messages
    messages = [{'role':'user', 'content':prompt}]
    # send prompt
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = messages
    )
    return response.choices[0]['message']['content'].strip()
    
def main():
    # 商品ページからテキストを取得
    input_text = scrape_all()
    # 入力分が長い場合は複数に分割
    split_texts = split_input_text(input_text)
    # GPTに入力用のプロンプトを作成
    extract_prompts = [str_template().format(text) for text in split_texts]
    # GPTの回答を取得
    authentication_openai()
    extract_texts = [send_prompt(prompt) for prompt in extract_prompts]

if __name__ == '__main__':
    main()