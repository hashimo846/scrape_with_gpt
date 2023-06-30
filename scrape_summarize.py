import requests
from bs4 import BeautifulSoup

# 商品ページのURL
HTML_URL = 'https://www.solarehotels.com/hotel/tochigi/chisuninn-kanuma/'
# 型番
MODEL_NUMBER = ''
# 入力テキスト（API制限等によりスクレイピングできないときに入力）
INPUT_TEXT = ''
# 1プロンプトあたりの上限の文字数
PROMPT_LIMIT = 2300

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

def str_question(model_number = MODEL_NUMBER):
    text = '今から与える入力を、2000文字以内に要約せよ。\n'
    text += '要約には'
    if MODEL_NUMBER != '': 
        text += '製品' + model_number + 'の'
    text += '定量的な数値情報や、商品の詳細や性能を示す情報は可能な限り含めてください。\n'
    text += 'また、入力の文が長いのため、<end>というまで出力を生成しないでください。\n'
    text += '<end>というまでは<ok>とだけ返答してください。\n'
    return text

def str_output():
    text = '#出力\n'
    text += '<end>'
    return text

def str_input(input_text):
    text = '#入力\n'
    text += input_text + '\n'
    return text

def str_prompt():
    input_text = scrape_all()
    prompt_text = '\n'.join([str_question(), str_input(input_text), str_output()])
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
    chat_count = 1
    print('\n\n#####Chat {}#######\n\n'.format(chat_count))
    prompt = str_prompt()
    prompt_list = split_prompt(prompt)
    print('\n\n##################\n\n'.join(prompt_list))

if __name__ == '__main__':
    main()