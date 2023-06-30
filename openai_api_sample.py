import os
import openai

# get available models
def str_model_list():
    for data in openai.Model.list()['data']:
        print(data['id'])

# authentication openai api
def authentication_openai():
    openai.organization = os.getenv("OPENAI_ORGANIZATION")
    openai.api_key = os.getenv("OPENAI_API_KEY")

# send prompt
def send_prompt(prompt=''):
    if not prompt:
        return
    else:
        # send prompt
        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo',
            messages = [
                {'role':'user', 'content':prompt},
            ],
        )
        return response.choices[0]['message']['content'].strip()

def main():
    authentication_openai() 
    print(send_prompt('なぜ空は青いのか?'))
    
if __name__ == '__main__':
    main()