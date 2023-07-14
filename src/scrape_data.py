from src import scrape_with_openai
from typing import List, Dict
from langchain.text_splitter import TokenTextSplitter
import openai
import os

# 入力テキスト（API制限等によりスクレイピングできないときに入力）
INPUT_TEXT = None
# 商品ページのURL
HTML_URL = 'https://www.jalan.net/yad389188/'
# 型番
MODEL_NUMBER = None
# 抽出項目（数値、文字列）
ITEM_LIST = ['最寄り駅', '周辺観光', 'チェックイン', 'チェックアウト', '料金']
# 1プロンプトに含む入力のトークン数の上限
INPUT_TOKEN_LIMIT = 3000
# 1プロンプトあたりの抽出項目数
ITEM_LIMIT = 4

def str_question(model_number:str, item_list:List[str], is_multi_prompt:bool) -> str:
    text = '今から入力と期待する出力形式を与えます。\n'
    text += '入力の情報のみを用いて、'
    if model_number != None: 
        text += '製品' + model_number + 'の'
    text += '、'.join(item_list)
    text += 'の情報を抜き出し、出力形式に従ってJSONで出力してください。\n'
    if is_multi_prompt:
        text += 'また、入力の文が長いのため、<end>というまで出力を生成しないでください。\n'
        text += '<end>というまでは<ok>とだけ返答してください。\n'
    return text

def str_format(item_list:List[str]) -> str:
    text = '#出力形式\n'
    text += '{\"' + '\":\"\",\"'.join(item_list) + '\":\"\"}' + '\n'
    return text

def str_output(is_multi_prompt:bool) -> str:
    text = '#出力'
    if is_multi_prompt:
        text += '\n<end>'
    return text

def str_input(input_text:str) -> str:
    text = '#入力\n'
    text += input_text + '\n'
    return text

def str_prompts(model_number:str, input_texts:List[str], item_list:List[str]) -> List[str]:
    is_multi_prompt = 1 < len(input_texts)
    prompts_list = []

    if is_multi_prompt:
        # first prompt
        prompt_text = '\n'.join([
            str_question(model_number, item_list, is_multi_prompt), 
            str_format(item_list), 
            str_input(input_texts[0]),
        ])
        prompts_list.append(prompt_text)
        # intermediate prompts
        for input_text in input_texts[1:-1]:
            prompts_list.append(input_text)
        # last prompt
        prompt_text = '\n'.join([
            input_texts[-1] + '\n',
            str_output(is_multi_prompt),
        ])
        prompts_list.append(prompt_text)
    else:
        # only one prompt
        prompt_text = '\n'.join([
            str_question(model_number, item_list, is_multi_prompt), 
            str_format(item_list), 
            str_input(input_texts[0]),
            str_output(is_multi_prompt),
        ])
        prompts_list.append(prompt_text)
    return prompts_list

# 入力を決められたトークン数ごとに分割する
def split_input_text(input_text:str, prompt_token_limit:int) -> List[str]:
    text_splitter = TokenTextSplitter(chunk_size=prompt_token_limit, chunk_overlap=0)
    texts = text_splitter.split_text(input_text)
    return texts

# OpenAI APIの認証
def authentication_openai():
    openai.organization = os.getenv("OPENAI_ORGANIZATION")
    openai.api_key = os.getenv("OPENAI_API_KEY")

# プロンプトを送信して回答を取得
def send_prompt(prompts):
    # make messages
    messages = [{'role':'user', 'content':prompts[0]}]
    for prompt in prompts[1:]:
        messages.append({'role':'assistant', 'content':'<ok>'})
        messages.append({'role':'user', 'content':prompt})

    # send prompt
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = messages
    )
    return response.choices[0]['message']['content'].strip()

def main():
    input_text = scrape_with_openai.scrape(url=HTML_URL,model_number=MODEL_NUMBER, input_text=INPUT_TEXT)
    split_inputs = split_input_text(input_text=input_text, prompt_token_limit=INPUT_TOKEN_LIMIT)
    item_idx = 0
    while item_idx < len(ITEM_LIST):
        print('\n\n##### {} #####\n\n'.format(','.join(ITEM_LIST[item_idx:item_idx+ITEM_LIMIT])))
        prompts = str_prompts(MODEL_NUMBER, split_inputs, item_list = ITEM_LIST[item_idx:item_idx+ITEM_LIMIT])
        print('\n\n##################\n\n'.join(prompts))
        print('\n\n###### answer ######\n\n')
        print(send_prompt(prompts))
        item_idx += ITEM_LIMIT

if __name__ == '__main__':
    main()