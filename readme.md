## lambda×コンテナイメージ×pythonでRSSリーダー×discord
- 純粋にRSSリーダーが欲しかった
    - 巡回するサイトが増えてきて、毎朝ブラウザからアクセスするのがなかなか面倒だった
### コンセプト
- VSCode Remote Containerを開発に導入してみる
- Lambdaのコンテナイメージサポートを使ってみる
- Cloudwatch Events利用によるLambda定期実行を試す
- AWSリソースから見やすいサービスに通知できるか試す(今回はDiscord)
### 構成図
- 
### 使い方
1. リポジトリをduplicate,cloneなどして自分のリポジトリにする
2. [この記事](https://dev.classmethod.jp/articles/github-action-ecr-push/)を参考にGithub ActionsでECRプッシュする設定を行う
    - バージョン運用は一旦置いておくため、[ECRにタグ付与する箇所はlatest固定にしています](https://github.com/mini-hiori/lambda-rss-reader-bot/blob/master/.github/workflows/main.yml)
3. Lambdaを新規作成する。コンテナイメージ利用を選択し、↑のECRのURIを指定する
4. [この記事](https://dev.startialab.blog/etc/a105)を参考に、↑のLambdaにEventbridgeによるトリガーを設定する
    - 周期はデフォルトはrate(1 hour)。変更する場合はget_rssに渡すinterval値も合わせて変更すること
5. [この記事](https://dev.classmethod.jp/articles/secure-string-with-lambda-using-parameter-store/#%E4%BB%8A%E3%81%AEwebhook-url%E3%81%AE%E6%89%B1%E3%81%84)を参考に、送りたいWebhookのURLをSystems Managerに配置する
    - 具体的には,以下を行う
        - KMSからCMKを作成する
        - Systems ManagerにWebhookのURLを登録する。このとき↑のCMKにより暗号化する
        - 3.のLambdaのIAMロールに、Systems ManagerのReadOnlyAccessと↑のCMKを利用した復号の権限を付与する
            - 後者は、kms:Decryptを付与すればよいが、AWS管理ポリシーに該当するものがないので自力でポリシーを作成する必要がある
                - [参考](https://qiita.com/minamijoyo/items/c6c6770f04c24a695081)

### 感想
- Lambda用コンテナをVSCode Remote Containerで直接開発に使うことはできた
    - VSCode開く際のビルドがだいぶ重いのがつらい
- Lambdaにコンテナでデプロイもできた ドキュメント通りなら難なく動くのでよかった
    - ☆ECRのURIを変えないままイメージの中身だけ変えた場合(latest固定など)、lambdaのコンテナイメージを空更新して再読み込みしないとlambdaに変更が反映されない場合がある
        - 短期間に連続実行した場合はlambdaのインスタンス(=コンテナ)が切り替わらないためな可能性が高い
- Lambdaの定期実行 via Eventbridgeもできた

### TODO
- Pythonの場合ベースイメージにalpineを使うのはやめたほうがいい。  
AWS公式のサンプルDockerfileがalpineだったので従ったが、buster系のほうが良いはず
    - https://future-architect.github.io/articles/20200513/
- ECRプッシュのトリガーにタグ使うのが若干面倒 もうちょっといい方法を探す
### よくわからんポイント
- Eventbridgeの実行開始タイミングが不明
    - 設定して1分くらいしたら勝手に動き始めたので普通に指定できない説が濃厚
