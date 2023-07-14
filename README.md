# このリポジトリは?
Webページからスクレイピングした情報を元に、更にChatGPTを用いて、抽出したい情報を抜き出す作業を半自動化したい。
そのためのスクリプトを作成するリポジトリ。
# 動作環境構築
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
docker-compose build --no-cache #少し時間がかかる
docker-compose up -d
```

# スクリプトの実行方法
仮想環境内はデフォルトで`/root`直下に移動しているので、次のコマンドで各スクリプトを実行できる。
```shell
docker-compose exec python3 python3 -m src.main
```