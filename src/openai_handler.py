import openai
import os
from typing import List

#使用するAIモデル
MODEL = os.getenv("OPENAI_MODEL")

# OpenAI APIの認証
def authentication() -> None:
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
            response = openai.ChatCompletion.create(model = MODEL,messages = messages)
        except (openai.error.APIError, openai.error.ServiceUnavailableError, APIConnectionError) as e:
            print('#Error: [{}}]{}'.format(type(e),e))
            sleep(5)
            print('#Retry: send prompt')
            continue
        else:
            # print('Success: send prompt')
            break
    return response.choices[0]['message']['content'].strip()