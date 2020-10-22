# 概要
CloudBuildの処理を設定するディレクトリ。

# 準備
## トリガーの作成
- `CloudBuild→トリガー→トリガーを作成`でairflowとfunctions用にそれぞれトリガーを作成。
- aiflowのトリガーには`_USER_INSTANCE` `_ZONE`変数を設定。
    - `_USER_INSTANCE`は`username@instancename`など
    - `_ZONE`は`us-west1-a`など

## 権限の設定
`CloudBuild→設定`から以下を有効化。

- CloudFunctions（CloudFunctions開発者）
- ComputeEngine（Computeインスタンス管理者）
- ServiceAccounts（サービスアカウントユーザー）
    - CloudFunctionsの有効化に際して推奨されたのでたぶん必要

