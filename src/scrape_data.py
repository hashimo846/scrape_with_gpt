
import requests
from bs4 import BeautifulSoup


# 商品ページのURL
HTML_URL = 'https://www.jalan.net/yad389188/'
# 型番
MODEL_NUMBER = ''
# 抽出項目（数値、文字列）
ITEM_LIST = ['最寄り駅', '周辺観光', 'チェックイン', 'チェックアウト', '料金']
# 入力テキスト（API制限等によりスクレイピングできないときに入力）
INPUT_TEXT = ''
# 要約した入力テキストかどうか
IS_SUMMARY = False
# 1プロンプトあたりの上限の文字数
PROMPT_LIMIT = 2300
# 1プロンプトあたりの抽出項目数
ITEM_LIMIT = 4

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

def str_question(model_number = MODEL_NUMBER, item_list = ITEM_LIST, is_summary = IS_SUMMARY):
    text = '今から入力と期待する出力形式を与えます。\n'
    text += '入力の情報のみを用いて、'
    if MODEL_NUMBER != '': 
        text += '製品' + model_number + 'の'
    text += '、'.join(item_list)
    text += 'の情報を抜き出し、出力形式に従ってJSONで出力してください。\n'
    if not is_summary:
        text += 'また、入力の文が長いのため、<end>というまで出力を生成しないでください。\n'
        text += '<end>というまでは<ok>とだけ返答してください。\n'
    return text

def str_format(item_list = ITEM_LIST):
    text = '#出力形式\n'
    text += '{\"' + '\":\"\",\"'.join(item_list) + '\":\"\"}' + '\n'
    return text

def str_output(is_summary = IS_SUMMARY):
    text = '#出力'
    if not is_summary:
        text += '\n<end>'
    return text

def str_input(input_text):
    text = '#入力\n'
    text += input_text + '\n'
    return text

def str_prompt(item_list = ITEM_LIST):
    input_text = scrape_all()
    prompt_text = '\n'.join([str_question(item_list=item_list), str_input(input_text), str_format(item_list=item_list), str_output()])
    return prompt_text

def split_prompt(prompt, prompt_limit=PROMPT_LIMIT):
    prompt_list = []
    start_idx = 0
    while start_idx < len(prompt):
        end_idx = start_idx + prompt_limit
        prompt_list.append(prompt[start_idx:end_idx])
        start_idx = end_idx
    return prompt_list
    
def main():
    item_idx = chat_count = 0
    while item_idx < len(ITEM_LIST):
        chat_count += 1
        print('\n\n#####Chat {}#######\n\n'.format(chat_count))
        prompt = str_prompt(item_list = ITEM_LIST[item_idx:item_idx+ITEM_LIMIT])
        prompt_list = split_prompt(prompt)
        print('\n\n##################\n\n'.join(prompt_list))
        item_idx += ITEM_LIMIT

if __name__ == '__main__':
    main()