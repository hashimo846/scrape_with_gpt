# このリポジトリは?
Webページからスクレイピングした情報を元に、更にChatGPTを用いて、抽出したい情報を抜き出す処理をしたい。
そのためのスクリプトを作成するリポジトリ。
# 動作環境構築
## OpenAI APIキーの設定
次のようにし、`env_file/.env`にAPIキー等の環境変数を設定。
```shell
cp env_file/.env.template env_file/.env
vi env_file/.env
```
# OpenAI API認証設定
GoogleのAPI設定から、サービスアカウント認証情報をJson形式でダウンロードし、`data/google_service_account.json`として保存する。
`data/google_service_account.json`の内容は次のようになっている。
```json
{
  "type": "service_account",
  "project_id": "******",
  "private_key_id": "******",
  "private_key": "******",
  "client_email": "******",
  "client_id": "******",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "******",
  "universe_domain": "googleapis.com"
}

```

## 仮想環境起動
次のコマンドにより、Docker環境を起動する。
```shell
docker-compose up -d
```
`requirements.txt`、`.env`、`Dockerfile`、`docker-compose.yml`を変更したときは、次のコマンドにより一度コンテナを削除してビルド。
```shell
docker-compose down
docker-compose build --no-cache #少し時間がかかる
docker-compose up -d
```

# スクリプトの実行方法
仮想環境内はデフォルトで`/root`直下に移動しているので、次のコマンドで各スクリプトを実行できる。
```shell
docker-compose exec python3 python3 -m src.main
```
