## lambda×コンテナイメージ×pythonでRSSリーダー×discord
- 純粋にRSSリーダーが欲しかった
    - 巡回するサイトが増えてきて、毎朝ブラウザからアクセスするのがなかなか面倒だった
### コンセプト
- VSCode Remote Containerを開発に導入してみる
- Lambdaのコンテナイメージサポートを使ってみる
- Cloudwatch Events利用によるLambda定期実行を試す
- Cloudwatch Events+Lambda環境をAWS CDKにて作成する
- AWSリソースから普段使いのサービスに通知できるか試す(今回はDiscord)
### 構成図
### 使い方
- Cloneする
- Docker buildしてECRにアップロード
- lambdaを新規作成し、↑のECRのエンドポイントを指定する
