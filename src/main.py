from src.extract import extract_boolean, extract_data, extract_option
from src import scrape
from src import summarize

# 商品情報
URL = 'https://www.jalan.net/yad389188/'
MODEL_NUMBER = None
INPUT_TEXT = None

# 抽出項目
DATA_ITEMS = ['最寄り駅', '周辺観光', 'チェックイン', 'チェックアウト', '料金']
BOOLEAN_ITEMS = ['無料Wi-Fi','部屋食','朝食あり','夕食あり','素泊まり','プール付き','ペット同伴可','バリアフリー対応','日帰り利用','記念日プラン']
OPTION_ITEMS = [
    {'name':'宿タイプ', 'options':['ビジネスホテル','シティホテル','リゾートホテル','旅館','ゲストハウス','コテージ','グランピング','キャンプ','ヴィラ','バンガロー','ロッジ']}, 
    {'name':'部屋タイプ', 'options':['シングル','ダブル','セミダブル','ツイン','トリプル','和室','和洋室']}, 
    {'name':'館内施設', 'options':['コインランドリー','ラウンジ','エステ','売店','バー']}, 
    {'name':'温泉の種類', 'options':['天然温泉','源泉かけ流し','露天風呂','客室露天風呂','大浴場','貸切風呂']}, 
    {'name':'メニュー', 'options':['ビュッフェ','和食','洋食','カフェ']},  
]

# メインプロセス
def main():
    full_text = scrape.scrape_all_text(url = URL, input_text=INPUT_TEXT)
    summarize_text = summarize.summarize(input_text = full_text)
    split_inputs = summarize.split_input(input_text = summarize_text)
    
    data_answers = extract_data.extract(split_inputs = split_inputs, model_number = MODEL_NUMBER, items = DATA_ITEMS)
    print('\n'.join(data_answers))
    boolean_answers = extract_boolean.extract(split_inputs = split_inputs, model_number = MODEL_NUMBER, items = BOOLEAN_ITEMS)
    print('\n'.join(boolean_answers))
    option_answers = extract_option.extract(split_inputs = split_inputs, model_number = MODEL_NUMBER, items = OPTION_ITEMS)
    print('\n'.join(option_answers))

if __name__ == '__main__':
    main()