from logging import DEBUG, INFO
from src import log
import openai
import os
from time import sleep
from typing import List

# ロガーの初期化
logger = log.init(__name__, DEBUG)

#使用するAIモデル
MODEL = os.getenv("OPENAI_MODEL")

# OpenAI APIの認証
openai.organization = os.getenv("OPENAI_ORGANIZATION")
openai.api_key = os.getenv("OPENAI_API_KEY")

# プロンプトを送信して回答を取得
def send(prompts:List[str]) -> str:
    # make messages
    messages = [{'role':'user', 'content':prompts[0]}]
    for prompt in prompts[1:]:
        messages.append({'role':'assistant', 'content':'<ok>'})
        messages.append({'role':'user', 'content':prompt})

    # send prompt
    while True:
        try:
            response = openai.ChatCompletion.create(model = MODEL,messages = messages, request_timeout = 30)
        except Exception as e:
            logger.error(log.format('プロンプト送信失敗', e))
            sleep(1)
            logger.info(log.format('プロンプト再送信中'))
            continue
        else:
            break
    return response.choices[0]['message']['content'].strip()