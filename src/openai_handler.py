import openai
import os
from time import sleep
from typing import List

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
            response = openai.ChatCompletion.create(model = MODEL,messages = messages, timeout = 10)
        except (openai.error.APIError, openai.error.ServiceUnavailableError, openai.error.APIConnectionError) as e:
            print('#Error: [{}]{}'.format(type(e),e))
            sleep(1)
            print('#Retry: プロンプト再送信中')
            continue
        except Exception as e:
            print('#Error: [{}]{}'.format(type(e),e))
            sleep(1)
            print('#Retry: プロンプト再送信中')
        else:
            break
    return response.choices[0]['message']['content'].strip()