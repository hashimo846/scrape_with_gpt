from logging import DEBUG, INFO
from src.extract import extract_boolean, extract_data, extract_option
from src import io_handler
from src import scrape
from src import summarize
from src import log

# ロガーの初期化
logger = log.init(__name__, DEBUG)

# メインプロセス
def main() -> None:
    # get input
    target_row_idx = 2
    sheet_url = io_handler.read_json()['sheet_url']
    logger.debug(log.format('入力情報', 'ターゲット行:{}\nスプレッドシートURL:{}'.format(target_row_idx, sheet_url)))

    # get all items from master
    master_items = io_handler.get_master_items(sheet_url)
    product = io_handler.get_product(sheet_url, target_row_idx)
    logger.debug(log.format('商品情報', product))

    # scrape all text from product url
    full_text = scrape.scrape_all_text(url = product['reference_url'], input_text=None)
    logger.debug(log.format('Webページから取得した全文', full_text))

    # summarize text
    summarize_text = summarize.summarize(input_text = full_text)
    logger.debug(log.format('要約文', summarize_text))

    # split input by token
    split_inputs = summarize.split_input(input_text = summarize_text)

    # extract each items
    data_answers = extract_data.extract(split_inputs = split_inputs, product_name = product['name'], items = master_items['data'])
    logger.debug(log.format('データ項目の抽出結果', data_answers))
    boolean_answers = extract_boolean.extract(split_inputs = split_inputs, product_name = product['name'], items = master_items['boolean'])
    logger.debug(log.format('Boolean項目の抽出結果', boolean_answers))
    option_answers = extract_option.extract(split_inputs = split_inputs, product_name = product['name'], items = master_items['option'])
    logger.debug(log.format('複数選択項目の抽出結果', option_answers))

    # output to spread sheet
    # io_handler.output_data(product = product, valid_columns = valid_columns, data_answers = data_answers)

        
if __name__ == '__main__':
    main()