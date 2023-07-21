from src.extract import extract_boolean, extract_data, extract_option
from src import io_handler
from src import scrape
from src import summarize

def print_log(title:str, content:str) -> None:
    print('======= {} ======='.format(title))
    print(content)

# メインプロセス
def main():
    # get product info from input json
    product_url, model_number, input_text = input_handler.get_product_info()
    # get all items from master
    items = input_handler.get_all_items()
    # scrape all text from product url
    full_text = scrape.scrape_all_text(url = product_url, input_text=input_text)
    print_log('full_text', full_text)
    # summarize text
    summarize_text = summarize.summarize(input_text = full_text)
    print_log('summarize_text', summarize_text)
    # split input by token
    split_inputs = summarize.split_input(input_text = summarize_text)
    # extract each items
    data_answers = extract_data.extract(split_inputs = split_inputs, model_number = model_number, items = items['data_items'])
    print_log('data_answers', data_answers)
    boolean_answers = extract_boolean.extract(split_inputs = split_inputs, model_number = model_number, items = items['boolean_items'])
    print_log('boolean_answers', boolean_answers)
    option_answers = extract_option.extract(split_inputs = split_inputs, model_number = model_number, items = items['option_items'])
    print_log('option_answers', option_answers)

if __name__ == '__main__':
    main()