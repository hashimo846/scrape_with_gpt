import requests
from bs4 import BeautifulSoup

# 商品ページのURL
HTML_URL = 'https://www.katoji-onlineshop.com/c/category/babygate/63423'
# 型番
MODEL_NUMBER = ''
# 抽出項目（数値、文字列）
ITEM_LIST = [
    {'item':'素材', 'option':['スチール製','プラスチック製','木製']},
    {'item':'ゲート種類', 'option':['扉','ロール','フェンス','置き型']},
    {'item':'ロック方法', 'option':['オートロック','ダブルロック']},
    {'item':'開閉方式', 'option':['両開き','片開き']},
    {'item':'設置方式', 'option':['壁取り付けタイプ（突っ張り式）','壁取り付けタイプ（ねじ式）','自立タイプ']},
    {'item':'適合基準', 'option':['SGマーク']},
]
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

def str_question(model_number = MODEL_NUMBER, item = None, is_summary = IS_SUMMARY):
    text = '今から入力、選択肢、期待する出力形式を与えます。\n'
    text += '入力のみを用いて、'
    if MODEL_NUMBER != '': 
        text += '製品' + model_number + 'の情報から、'
    text += item['item'] + 'を選択肢の中から複数選択し、出力形式に従ってJSONで出力してください。\n'
    text += 'もし選択肢の中に該当するものがない場合は、出力形式に従って空の文字列をJSONで出力してください。\n'
    if not is_summary:
        text += 'また、入力の文が長いのため、<end>というまで出力を生成しないでください。\n'
        text += '<end>というまでは<ok>とだけ返答してください。\n'
    return text

def str_option(item = None):
    text = '#選択肢\n'
    text += '、'.join(item['option']) + '\n'
    return text

def str_format(item = None):
    text = '#出力形式\n'
    text += '{\"' + item['item'] +'\":[\"\",\"\"]}' + '\n'
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

def str_prompt(item = None):
    input_text = scrape_all()
    prompt_text = '\n'.join([
        str_question(item=item), 
        str_option(item=item),
        str_format(item=item), 
        str_input(input_text),
        str_output(),
    ])
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
    for chat_count in range(len(ITEM_LIST)):
        print('\n\n#####Chat {}#######\n\n'.format(chat_count+1))
        prompt = str_prompt(item = ITEM_LIST[chat_count])
        prompt_list = split_prompt(prompt)
        print('\n\n##################\n\n'.join(prompt_list))

if __name__ == '__main__':
    main()