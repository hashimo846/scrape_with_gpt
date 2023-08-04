from src.extract import extract_boolean, extract_data, extract_option
from src import io_handler
from src import scrape
from src import summarize

def print_log(title:str, content:str) -> None:
    print('\n======= {} =======\n'.format(title))
    print(content)

# メインプロセス
def main() -> None:
    # get input
    target_row_idx = 2
    sheet_url = io_handler.read_json()['sheet_url']
    print_log('スプレッドシートURL', sheet_url)

    # get all items from master
    items = io_handler.get_all_items(sheet_url)
    product = io_handler.get_product(sheet_url, target_row_idx)

    print_log('商品情報', product)
    # scrape all text from product url
    full_text = scrape.scrape_all_text(url = product['reference_url'], input_text=None)
    print_log('Webページから取得した全文', full_text)

    # summarize text
    summarize_text = summarize.summarize(input_text = full_text)
    print_log('要約文', summarize_text)

    # split input by token
    split_inputs = summarize.split_input(input_text = summarize_text)

    # extract each items
    data_answers = extract_data.extract(split_inputs = split_inputs, product_name = product['name'], items = items['data_items'])
    print_log('データ項目の抽出結果', data_answers)
    boolean_answers = extract_boolean.extract(split_inputs = split_inputs, product_name = product['name'], items = items['boolean_items'])
    print_log('Boolean項目の抽出結果', boolean_answers)
    option_answers = extract_option.extract(split_inputs = split_inputs, product_name = product['name'], items = items['option_items'])
    print_log('複数選択項目の抽出結果', option_answers)

    # output to spread sheet
    # io_handler.output_data(product = product, valid_columns = valid_columns, data_answers = data_answers)

        
if __name__ == '__main__':
    main()