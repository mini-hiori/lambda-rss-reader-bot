## lambda×コンテナイメージ×pythonでRSSリーダー×discord
- 純粋にRSSリーダーが欲しかった
    - 巡回するサイトが増えてきて、毎朝ブラウザからアクセスするのがなかなか面倒だった
### コンセプト
- VSCode Remote Containerを開発に導入してみる
- Lambdaのコンテナイメージサポートを使ってみる
- Cloudwatch Events利用によるLambda定期実行を試す
- AWSリソースから見やすいサービスに通知できるか試す(今回はDiscord)
### 使い方
- リポジトリをduplicate,cloneなどして自分のリポジトリにする
- [この記事](https://dev.classmethod.jp/articles/github-action-ecr-push/)を参考にGithub ActionsでECRプッシュする設定を行う
    - バージョン運用は一旦置いておくため、[ECRにタグ付与する箇所はlatest固定にしています](https://github.com/mini-hiori/lambda-rss-reader-bot/blob/master/.github/workflows/main.yml)
- Lambdaを新規作成する。コンテナイメージ利用を選択し、↑のURIを指定する
- [この記事](https://dev.startialab.blog/etc/a105)を参考に、↑のLambdaにEventbridgeによるトリガーを設定する
    - 周期はデフォルトはrate(1 hour)。変更する場合はget_rssに渡すinterval値も合わせて変更すること
- [この記事](https://dev.classmethod.jp/articles/secure-string-with-lambda-using-parameter-store/#%E4%BB%8A%E3%81%AEwebhook-url%E3%81%AE%E6%89%B1%E3%81%84)を参考に、送りたいWebhookのURLをSystems Managerに配置する

### 感想
- Lambda用コンテナをVSCode Remote Containerで直接開発に使うことはできた
    - VSCode開く際のビルドがだいぶ重いのがつらい
- Lambdaにコンテナでデプロイもできた ドキュメント通りなら難なく動くのでよかった
    - ECRにpushしとけばそれでリリース終わりなのはLambdaの利点
        - ECSでいうところのタスク再起動等の手間がない
- Lambdaの定期実行 via Eventbridgeも多分できた？
    - https://dev.startialab.blog/etc/a105

### TODO
- Pythonの場合ベースイメージにalpineを使うのはやめたほうがいい。buster系に置換できればベスト
    - https://future-architect.github.io/articles/20200513/
- ECRプッシュのトリガーはタグ指定なしのビルドも含めていい？
### よくわからんポイント
- Eventbridgeの実行開始タイミングが不明
    - 設定して1分くらいしたら勝手に動き始めたので普通に指定できない説が濃厚
