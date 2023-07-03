# このリポジトリは?
Webページからスクレイピングした情報を元に、更にChatGPTを用いて、抽出したい情報を抜き出す作業を半自動化したい。
そのためのスクリプトを作成するリポジトリ。
# 使い方
## APIキーの設定
次のようにし、`.env`にAPIキー等の環境変数を設定。
```shell
cp .env.template .env
vi .env
```

## 仮想環境起動
次のコマンドにより、Docker環境を起動する。
```shell
docker-compose up -d
```
`requirements.txt`、`.env`、`Dockerfile`、`docker-compose.yml`を変更したときは、次のコマンドにより一度コンテナを削除してビルド。
```shell
docker-compose down
docker-compose build
docker-compose up -d
```

## スクリプトの実行
仮想環境内ではデフォルトで`src/`直下に移動しているので、次のコマンドで各スクリプトを実行できる。
```shell
docker-compose exec python3 python3 <実行したいスクリプト>
```

# スクリプトの説明
## scrape_extract.py
実行すると、指定したWebページからスクレイピングした情報を元に、GPTにて対象の情報を抽出するためのプロンプトを生成する。

実行に必要なパラメータは次である。

* HTML_URL:抽出対象の情報が記載されている商品ページのURL
* MEDEL_NUMBER:抽出対象の製品の型番（型番がない商品は''を入力）
* ITEM_LIST：抽出項目のリスト（抽出対象が数値、文字列のもののみ可能）
* INPUT_TEXT：入力テキスト（API制限等でスクレイピングできないときに入力）
* IS_SUMMARY:入力テキストが要約されたものかどうか（プロンプトが複数に分割されるかどうか）
* PROMPT_LIMIT：1プロンプトあたりの上限の文字数
* ITEM_LIMIT：1プロンプト抽出する項目数の最大

## scrape_summarize.py
実行すると、指定したWebページからスクレイピングした情報を、1プロンプトに収まるように要約してくれる。
この際、対象商品に関する定量的な情報等は極力欠損しないようにしているが、GPTの仕様の都合上、必要な情報が抜け落ちる可能性もある。

実行に必要なパラメータは次である。

* HTML_URL:抽出対象の情報が記載されている商品ページのURL
* MEDEL_NUMBER:抽出対象の製品の型番（型番がない商品は''を入力）
* INPUT_TEXT：入力テキスト（API制限等でスクレイピングできないときに入力）
* PROMPT_LIMIT：1プロンプトあたりの上限の文字数

## openai_api_sample.py
OpenAIのAPIの動作を確認するスクリプト。

実行するには、事前に環境変数の設定が必要。
```shell
export OPENAI_ORGANIZATION="Organization ID"
export OPENAI_API_KEY="API Key"
```
実行すると、質問に対する回答が出力される。