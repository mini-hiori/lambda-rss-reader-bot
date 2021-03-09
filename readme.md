## lambda×コンテナイメージ×pythonでRSSリーダー×discord
- 純粋にRSSリーダーが欲しかった
    - 巡回するサイトが増えてきて、毎朝ブラウザからアクセスするのがなかなか面倒だった
### コンセプト
- VSCode Remote Containerを開発に導入してみる
- Lambdaのコンテナイメージサポートを使ってみる
- Cloudwatch Events利用によるLambda定期実行を試す
- AWSリソースから見やすいサービスに通知できるか試す(今回はDiscord)
### 構成図
![](https://github.com/mini-hiori/zenn-content/blob/main/images/lambda-rss-reader-bot/architecture.png?raw=true)
### 使い方
1. リポジトリをduplicate,cloneなどして自分のリポジトリにする
2. [この記事](https://dev.classmethod.jp/articles/github-action-ecr-push/)を参考にGithub ActionsでECRプッシュする設定を行う
    - バージョン運用は一旦置いておくため、[ECRにタグ付与する箇所はlatest固定にしています](https://github.com/mini-hiori/lambda-rss-reader-bot/blob/master/.github/workflows/main.yml)
3. Lambdaを新規作成する。コンテナイメージ利用を選択し、↑のECRのURIを指定する
4. [この記事](https://dev.startialab.blog/etc/a105)を参考に、↑のLambdaにEventbridgeによるトリガーを設定する
    - 周期はデフォルトはrate(1 hour)。変更する場合はget_rssに渡すinterval値も合わせて変更すること
5. [この記事](https://dev.classmethod.jp/articles/secure-string-with-lambda-using-parameter-store/#%E4%BB%8A%E3%81%AEwebhook-url%E3%81%AE%E6%89%B1%E3%81%84)を参考に、以下2つをSystems Managerパラメータストアに配置する
    1. 送りたいDiscord-WebhookのURL
        - 暗号化して配置したいので、先にKMSから暗号化キー(CMK)を作成して暗号化する
    2. RSS取得先リンク(改行で区切って列挙する)
        - こちらは平文でOK
6. 5.の記事を参考に、3.LambdaのロールにSSM参照権限とCMKを利用した復号の権限を付与する
    - SSM参照権限→SSMReadOnlyAccessでOK
    - 後者はkms:Decrypt。AWS管理ポリシーに該当するものがないので自力でポリシーを作成する必要がある
        - [参考](https://qiita.com/minamijoyo/items/c6c6770f04c24a695081)

### TODO
- Pythonの場合ベースイメージにalpineを使うのはやめたほうがいい。  
AWS公式のサンプルDockerfileがalpineだったので従ったが、buster系のほうが良いはず
    - https://future-architect.github.io/articles/20200513/
- ECRプッシュのトリガーにタグ使うのが若干面倒
### よくわからんポイント
- Eventbridgeの実行開始タイミングが不明
    - 設定して1分くらいしたら勝手に動き始めたので普通に指定できない説が濃厚
