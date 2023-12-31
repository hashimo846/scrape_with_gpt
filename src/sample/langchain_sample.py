from langchain.document_loaders.image import UnstructuredImageLoader
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.chat_models import ChatOpenAI
import os

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, max_tokens=1000)
text_splitter = CharacterTextSplitter(chunk_size=1000)

state_of_the_union = 'ーカーチャイルドシートトラベルシステム室内用品nuna｜ヌナnunaブランドすべての商品ベビーキャリアベビーカーチャイルドシートトラベルシステム室内用品hugme｜ハグミーmonpoke｜モンポケPREMIUMLINE｜プレミアムラインNewYork・Baby｜ニューヨーク・ベビーシーンから選ぶ出産前にそろえておきたいもの腰が座ったら必要なもの離乳食がはじまったら必要なもの出産祝いギフトセット旅行・ご実家で雨の日に大活躍！レインカバー付き赤ちゃんの感染対策・ウイルス対策カラーから選ぶホワイトグレーブラックベージュブラウングリーンブルーオレンジレッドピンクイエロー最近チェックした商品インフォメーションご利用ガイドよくある質問お問い合わせ会社概要特定商取引法に基づく表示プライバシーポリシーHOMEカテゴリーから選ぶベビーゲートカトージベビーセーフティオートゲート高さ78cmのオートクローズ・ダブルロック機能付きベビーゲートキッチンや階段下に設置して安心安全【76～85.5cm幅に対応】サービスクリーニングサービスRental組立配送サービスカテゴリーから選ぶSALEベビーベッドベビーベッド（70×120cm）ミニベビーベッド（60×90cm）ミニミニベビーベッド（50×70cm）ベビーベッドと布団のセット（70×120cm）ミニベビーベッドと布団のセット（60×90cm）寝具ベビー布団（70×120cm）ミニベビー布団（60×90㎝）ミニミニベビー布団（50×70cm）寝具その他バウンサーハイローラックベビーキャリアベビーカー両対面式背面式オプション・その他二人乗り・多人数乗りベビーカートラベルシステムベース無しプランベース付きプラン12歳までの完全プランチャイルドシート0歳～1歳頃まで使える0歳～4歳まで使える0歳～7歳まで使える0歳～12歳頃まで使える1歳～12歳頃まで使える3歳～12歳頃まで使えるベビーチェアハイチェアローチェアテーブルチェアチェアその他ベビーチェアとクッションのセットベビーサークル(遊び場＆お昼寝)ジュニアシートベビーゲートベビーゲート本体ベビーゲートオプション歩行器テーブル&チェアオムツポット保育用品カープレート等カープレートステッカー日本製価格から選ぶ～2,000円2,001円～5,000円5,001円～10,000円10,001円～30,000円30,001円以上ブランドから選ぶjoie｜ジョイーnuna｜ヌナhugme｜ハグミーNewYork・Baby｜ニューヨーク・ベビーmonpoke｜モンポケPREMIUMLINE｜プレミアムラインシーンから選ぶ出産前にそろえておきたいもの腰が座ったら必要なもの離乳食がはじまったら必要なもの旅行・ご実家で雨の日に大活躍！レインカバー付き赤ちゃんの感染対策・ウイルス対策カラーから選ぶホワイトグレーブラックベージュブラウングリーンブルーレッドオレンジピンクイエロー雑誌・メディア掲載画像拡大カトージがおすすめする突っ張り式のベビーゲートカトージベビーセーフティオートゲート高さ78cmのオートクローズ・ダブルロック機能付きベビーゲートキッチンや階段下に設置して安心安全【76～85.5cm幅に対応】送料無料商品番号63423¥5,478税込送料パターンB：送料無料/北海道・沖縄・離島部は除く→詳しい送料はこちらでご確認ください。▼ウォールキャップのご購入はこちらからお気に入り登録12345678910+カートに入れる動画で紹介ベビーゲートの取り付け方▼セール開催2023年7月1日(土)〜2023年7月17日(月)までセール！セール対象商品はこちらからご覧ください▼▼▼ただいまレビューキャンペーン開催中▼Tweet商品についてのお問い合わせ拡張性の高い、シンプルデザインのスチールゲートです。▼Sサイズ、Mサイズ、Lサイズ、拡張フレームやセット商品もご用意しています。商品番号63423使用対象生後24ヶ月以下のお子様取付幅75～85cm※取付場所に幅木がある場合、幅木の高さが約1cm以上、約4.5cm以下の場所へは、しっかり取付ができない事がある為、ご使用いただけません。設置方式つっぱりタイプ商品サイズ幅73×奥行き4.5×高さ79cm商品重量4.7kg梱包サイズ75×5×82.5cm梱包重量5.4kg素材鋼鉄フレームABS樹脂塗装エポキシ樹脂塗装機能＊扉を一定以上開いた状態から手を離すと、自動で扉が閉まります。（オートクローズ機能）＊扉を90°程開けると、そのまま開いた状態になります。（扉開放機能）＊扉を開く時は、2段ロック式なので、お子様は開きにくい仕様です。（安心2段ロック）取付上の注意事項■取付ける壁面の幅は6cm以上必要です。6cm以下の場所へは、取付いただけません。■取付ける壁面に対して、ゲートが直角に取付できない場所へは、取付いただけません。■階段の上には、取付いただけません。■ゲートを取り付ける壁面が弱い場合は、壁面が凹んだり、抜けたりする恐れがありますのでご注意ください。■柱もしくは、壁の中に柱がある場所に取付けてください。■壁につっぱって取付ける仕様となりますので、壁紙が剥がれたり、壁に取付け跡が残る場合がございます。■取付場所に幅木がある場合、幅木の高さが約1cm以上、約4.5cm以下の場所へは、しっかり取付ができない事がある為、ご使用いただけません。※取扱説明書の、取扱説明、注意事項をご確認の上、正しくお取り付けください。使用上の注意事項■'

texts = text_splitter.split_text(state_of_the_union)

docs = [Document(page_content=t) for t in texts]

MODEL_NUMBER = ''
template = '今から与える入力のみを用いて、\n'
if MODEL_NUMBER != '': 
    template += '製品' + model_number + 'の'
template += '製品の詳細・性能を示す情報や、定量的な数値情報を抽出してください。\n\n'
template += '入力：{text}'
prompt = PromptTemplate(input_variables=['text'], template=template)
chain = load_summarize_chain(llm, chain_type="map_reduce",map_prompt=prompt, combine_prompt=prompt, verbose=False)
print(chain.run(docs))