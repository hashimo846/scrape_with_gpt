from bs4 import BeautifulSoup
from langchain.text_splitter import TokenTextSplitter
import openai
import os
import requests

SAMPLE_DATA = {
    # 商品ページのURL
    'url':'https://www.katoji-onlineshop.com/c/category/babygate/63423',
    # 型番
    'model_number':None
}

# 1プロンプトに含む入力のトークン数の上限
PROMPT_TOKEN_LIMIT = 3500
# 入力を分割する際の重複するトークン数
TOKEN_OVERLAP = 100

# 商品ページから全テキストを取得
# (ページからテキストを抽出できない場合は手動でinput_textを入力)
def get_all_text(url, input_text = None):
    # URLからページを取得
    with requests.get(url) as r:
        html = BeautifulSoup(r.content, 'html.parser')
    # ページから文字列を抽出 or 引数から文字列を抽出
    if input_text == None:
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
def split_input_text(input_text, prompt_token_limit = PROMPT_TOKEN_LIMIT, token_overlap = TOKEN_OVERLAP):
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
def scrape(url, model_number = None, input_text = None, is_service = False):
    # 商品ページからテキストを取得
    input_text = get_all_text(url=url, input_text=input_text)
    # 入力分が長い場合は複数に分割
    split_texts = split_input_text(input_text)
    # GPTに入力用のプロンプトを作成
    scrape_prompts = [str_template(model_number).format(text) for text in split_texts]
    # GPTの回答を取得
    authentication_openai()
    extract_texts = [send_prompt(prompt) for prompt in scrape_prompts]
    # 回答を結合
    extract_text = '\n'.join(extract_texts)
    return extract_text

def main():
    # 商品ページからテキストを取得
    input_text = get_all_text(url=SAMPLE_DATA['url'], model_number=SAMPLE_DATA['model_number'])
    # 入力文が長い場合は複数に分割
    split_texts = split_input_text(input_text)
    # GPTに入力用のプロンプトを作成
    extract_prompts = [str_template().format(text) for text in split_texts]
    # GPTの回答を取得
    authentication_openai()
    extract_texts = [send_prompt(prompt) for prompt in extract_prompts]
    # 回答を結合
    extract_text = '\n'.join(extract_texts)

if __name__ == '__main__':
    main()