from langchain.text_splitter import TokenTextSplitter
from src import openai_handler
from typing import List, Dict

# プロンプト中の質問部分の文字列を返す
def str_question(product_name:str, item:Dict, is_multi_prompt:bool) -> str:
    text = '今から入力、選択肢、期待する出力形式を与えます。\n'
    text += '入力のみを用いて、' + product_name + 'について、'
    text += item['name'] + 'を選択肢の中から複数選択し、出力形式に従ってJSONで出力してください。\n'
    text += 'もし選択肢の中に該当するものがない場合は、出力形式に従って空の文字列を出力してください。\n'
    text += 'また、選択肢にないものは出力に含めないでください。\n'
    if is_multi_prompt:
        text += 'また、入力の文が長いのため、<end>というまで出力を生成しないでください。\n'
        text += '<end>というまでは<ok>とだけ返答してください。\n'
    return text

# プロンプト中の選択肢部分の文字列を返す
def str_option(item:Dict) -> str:
    text = '#選択肢\n'
    text += '- '
    text += '\n- '.join(item['options']) + '\n'
    return text

# プロンプト中の出力形式部分の文字列を返す
def str_format(item:Dict) -> str:
    text = '#出力形式\n'
    text += '{\"' + item['name'] +'\":[\"\",\"\"]}' + '\n'
    return text

# プロンプト中の出力部分の文字列を返す
def str_output(is_multi_prompt:bool) -> str:
    text = '#出力'
    if is_multi_prompt:
        text += '\n<end>'
    return text

# プロンプト中の入力部分の文字列を返す
def str_input(input_text:str) -> str:
    text = '#入力\n'
    text += input_text + '\n'
    return text

# 生成したプロンプトのリスト返す
def str_prompts(product_name:str, item:Dict, input_texts:List[str]) -> List[str]:
    is_multi_prompt = 1 < len(input_texts)
    prompts_list = []
    
    if is_multi_prompt:
        # first prompt
        prompt_text = '\n'.join([
            str_question(product_name, item, is_multi_prompt), 
            str_option(item),
            str_format(item), 
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
            str_question(product_name, item, is_multi_prompt), 
            str_option(item),
            str_format(item), 
            str_input(input_texts[0]),
            str_output(is_multi_prompt),
        ])
        prompts_list.append(prompt_text)
    return prompts_list

# 対象項目の情報を抽出
def extract(split_inputs:List[str], product_name:str, items:List[Dict]) -> List[str]:
    answers = []
    for item in items:
        prompts = str_prompts(product_name, item, split_inputs)
        answers.append(openai_handler.send(prompts))
    return answers
