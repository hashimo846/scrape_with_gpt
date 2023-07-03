import requests
from bs4 import BeautifulSoup

# 商品ページのURL
HTML_URL = 'https://www.amazon.co.jp/dp/B08BP6894V'
# 型番
MODEL_NUMBER = ''
# 抽出項目（数値、文字列）
ITEM_LIST = [
    {'item':'ベッドサイズ', 'option':['シングル','セミダブル','セミシングル','ダブル','クイーン','キング']},
    {'item':'タイプ', 'option':['高反発','低反発','折りたたみ','アンダーマットレス','マットレストッパー','ボンネスコイル','ポケットコイル']},
    {'item':'収納方法', 'option':['三つ折り','ロール']},
    {'item':'中材', 'option':['ポリウレタンフォーム','ファイバー','ラテックス']},
    {'item':'カバー素材', 'option':['ナイロン','ポリエステル','綿','ウール']},
    {'item':'利用場所', 'option':['ベッド','床']},
    {'item':'商材', 'option':['ジェルマットレス']},
]
# 入力テキスト（API制限等によりスクレイピングできないときに入力）
INPUT_TEXT = 'サイズ	ダブル（140*200*3cm） 特徴	防臭, 高反発 商品の硬さ	硬め ブランド	Novilla 商品の寸法	2L x 1.4W x 0.03Th m 色	ホワイト モデル名	FXNV0JD801-D この商品について 【竹炭入りです防臭効果】日本の多湿気候を考慮し、竹炭入りの表面生地を採用します。やさしい手触りで心を癒やし、防臭加工でウレタン特有の臭いも軽減します。 【高反発力＆耐久性】外国から輸入された高品質のウレタンフォームを採用し、高い弾力性と良い復元性を持って、体をよく支えます。さらに、安心で確かな品質を実現するために、弊社は耐久性試験を行いました。100K荷重を数万回繰り返し加圧するという耐荷重試験をクリアした製品です。 【カバーは水洗い可】ファスナー付きのカバーは洗えるので、溜まっている寝汗の湿気と皮脂の汚れを気楽に対応できます。洗濯便利でマットレスを清潔に使い続けます！ 【滑らかで柔らかな肌触り】:表面には高級感のあるニット生地を使用。柔らかい手触りと伸縮性に優れ、快適な寝心地をご提供。竹炭入りで吸湿防臭機能があり、オールシーズン快適にお休みいただけます。静電気と毛玉防止加工を施しているのでマットレスカバーの耐久性が更にアップします。 【様々なシーンで活躍】高反発なので底付き感がなく、直接床やベッドのうえに敷いても快適です。コンパクトに収納できるため、急な来客用にも便利です。 【製品の仕様】ダブルサイズ(D):幅140cm×奥行200cm×厚さ3cm;パッケージ内容：マットレス本体×1、 日本語説明書×1 、保証書×1。ご不明な点がありましたら、いつでもお気軽に当店までお問い合わせください。Novillaは20～60代の働く男女を対象に「睡眠に関する調査」を実施して、働く世代の睡眠の悩みをを深く認識しています。日本人好みの硬さを追求して、この「硬めの160N×高密度30D」マットレスが登場した！高品質と高耐久性の特徴で皆様に愛されています。ここ数年間ででアメリカ・カナダ・イギリス・中東の 100万人以上のお客様に快適な眠りを提供させていただきました。朝までぐっすり熟睡したい方へおススメです！ 【厚さ3/5cm✕独自専門技術✕硬め160N✕高密度30Dウレタン】マットレス！ マットレス 商品詳細をご紹介 サイズ： シングル：幅100cm×奥行200cm×高さ３cm シングル：幅100cm×奥行200cm×高さ5cm セミダブル：幅120cm×奥行200cm×高さ3cm セミダブル：幅120cm×奥行200cm×高さ5cm ダブル：幅140cm×奥行200cm×高さ3cm ダブル：幅140cm×奥行200cm×高さ5cm カバー生地：ポリエステル100％ 詰め物：高反発・高密度ウレタン 搬入便利：軽量なので持ち運び便利！来客用のベッドとしても活躍する便利アイテムです。ゆっくり本を読んたり、テレビを見たり、休みを快適に過ごし～ そのほかのポイント↓： 硬すぎず、柔らかすぎず 選べる2つの厚さ このマットレスは高反発のウレタンによって適度な柔らかさを実現しているので、寝心地が良いです。 マットレスの詳細 1 2 マットレス 4 自然の知恵-竹炭パワー 湿気を貯めない秘訣→ベッドマットのカバーには竹炭成分を注入。消臭吸湿性に優れた竹炭入りの生地で発汗による湿気と臭いを吸収、一晩中さわやかな寝心地を保ちます。 やや硬めの高反発素材 硬さ160N(ニュートン)の高反発素材を採用しており、やや硬めの寝心地で腰や肩など、疲れを感じやすい体のパーツへの負担が軽減されやすくなります。 寝返りが多い方や仰向けに寝ることが多い方にオススメなマットレスです。理想の寝姿勢をキープ！ 二重カバー 溜まっている寝汗の湿気と皮脂の汚れを気楽に対応できるように、二重カバーのデザインを応用します。外カバーはファスナー付きますので、取り外して洗濯でき、いつでも清潔にお使い頂けます。 インナーカバーも付いており、ウレタンフォーム自体劣化防止も確保できます。​ 裏面には滑り止め加工され、寝る時ズレにくいです。 圧縮梱包 搬入および環境への配慮からロール状に圧縮されたコンパクトな状態で梱包しています。 狭い道路や扉でもスムーズに搬入可能となり、使い場所まで楽に運べます。 体全体を支え、至福の眠りを体験できる ベッドマット 心地よい眠りに導くためのこだわり 高反発素材を採用しており、優れたクッション性と復元性を兼ね備えています。 横になると体圧によって一度は沈みますが、すぐ体圧を均一に分散させて押し上げて、しっかりと身体全体をホールドし、包み上げてくれるのです。 体圧分散性が高いマットレスですから横む向きでも仰向けでも正しい寝姿勢を保つことができ、腰にも負担がかからなくなります。 重さの違う部位を適切に支えるため、背骨がS字にカーブしています。独自高反発素材で身体のS字ラインに合わせて体圧を分散し、理想的な体型での眠りをサポートします。柔・硬・軟の三つの要素がバランスよく作用し合うことで理想的な寝姿勢を保ち。眠りが浅い人にもおすすめ。 マットレス シングル 高品質は弛まぬ研究開発と徹底した品質管理から ①CertiPUR-US特定の基準を満たしているフォームを採用。またオゾン消費剤、PBDES、TDCPP、TCEP難燃剤、水銀、鉛、重金属などの環境・人体に害がある成分は使用しておりません。赤ちゃんから大人までご利用いただけます。 ②10年品質保証 商品に万が一の不具合がございましたらお気軽に購入履歴よりお問い合わせください。 圧縮梱包で搬入便利 5cm  高反発マットレス ロール式圧縮梱包でコンパクト配送 パッケージ内容： ベットマットレス×1 日本語説明書×1 開封用カッター×1 保証書×1 ご注意： ▲本商品はマットレスのみです。 ▲商品写真はできる限り実物の色に近づけるよう徹底しておりますが、 お使いのモニター設定、お部屋の照明等により実際の商品と色味が異なる場合がございます。 ▲生産時期により、色・サイズ・デザインが多少が異なる場合がございます。あらかじめ御了承下さい。 ▲商品到着後、品質確認の為に7日以内に必ず開封してください。'
# 要約した入力テキストかどうか
IS_SUMMARY = False
# 1プロンプトあたりの上限の文字数
PROMPT_LIMIT = 2300
# 1プロンプトあたりの抽出項目数
ITEM_LIMIT = 4

def scrape_all(url = HTML_URL, input_text = INPUT_TEXT):
    # URLからページを取得
    with requests.get(url) as r:
        html = BeautifulSoup(r.content, 'html.parser')
    # ページから文字列を抽出 or 引数から文字列を抽出
    if input_text == '':
        text = html.text
    else:
        text = input_text
    # テキストのみ抽出
    text = ''.join(text.split(' '))
    text = ''.join(text.split('　'))
    text = ''.join(text.split('\n'))
    text = ''.join(text.split('\t'))
    text = ''.join(text.split('\r'))
    text = ''.join(text.split('\v'))
    text = ''.join(text.split('\f'))
    return text

def str_question(model_number = MODEL_NUMBER, item = None, is_summary = IS_SUMMARY):
    text = '今から入力、選択肢、期待する出力形式を与えます。\n'
    text += '入力のみを用いて、'
    if MODEL_NUMBER != '': 
        text += '製品' + model_number + 'の情報から、'
    text += item['item'] + 'を選択肢の中から複数選択し、出力形式に従ってJSONで出力してください。\n'
    text += 'もし選択肢の中に該当するものがない場合は、出力形式に従って空の文字列をJSONで出力してください。\n'
    if not is_summary:
        text += 'また、入力の文が長いのため、<end>というまで出力を生成しないでください。\n'
        text += '<end>というまでは<ok>とだけ返答してください。\n'
    return text

def str_option(item = None):
    text = '#選択肢\n'
    text += '、'.join(item['option']) + '\n'
    return text

def str_format(item = None):
    text = '#出力形式\n'
    text += '{\"' + item['item'] +'\":[\"\",\"\"]}' + '\n'
    return text

def str_output(is_summary = IS_SUMMARY):
    text = '#出力'
    if not is_summary:
        text += '\n<end>'
    return text

def str_input(input_text):
    text = '#入力\n'
    text += input_text + '\n'
    return text

def str_prompt(item = None):
    input_text = scrape_all()
    prompt_text = '\n'.join([
        str_question(item=item), 
        str_option(item=item),
        str_input(input_text),
        str_format(item=item), 
        str_output(),
    ])
    return prompt_text

def split_prompt(prompt, prompt_limit=PROMPT_LIMIT):
    prompt_list = []
    start_idx = 0
    while start_idx < len(prompt):
        end_idx = start_idx + prompt_limit
        prompt_list.append(prompt[start_idx:end_idx])
        start_idx = end_idx
    return prompt_list
    
def main():
    for chat_count in range(len(ITEM_LIST)):
        print('\n\n#####Chat {}#######\n\n'.format(chat_count+1))
        prompt = str_prompt(item = ITEM_LIST[chat_count])
        prompt_list = split_prompt(prompt)
        print('\n\n##################\n\n'.join(prompt_list))

if __name__ == '__main__':
    main()