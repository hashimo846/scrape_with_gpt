import openai
import os

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
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = messages
    )
    return response.choices[0]['message']['content'].strip()