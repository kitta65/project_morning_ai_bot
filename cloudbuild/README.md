# 概要
CloudBuildの処理を設定するディレクトリ。

# 準備
## トリガーの作成
- airflowとfunctions用にそれぞれCloudBuildのトリガーを作成。
- aiflowのトリガーには`_USER_INSTANCE` `_ZONE`変数を設定。
    - `_USER_INSTANCE`は`username@instancename`など
    - `_ZONE`は`us-west1-a`など

## 権限の設定
CloudBuild管理画面の設定から以下を有効化。

- CloudFunctions（CloudFunctions開発者）
- ComputeEngine（Computeインスタンス管理者）
- ServiceAccounts（サービスアカウントユーザー）
    - CloudFunctionsの有効化に際して推奨されたのだが、必要か要確認

# 注意
- 初回のみ未認証の関数呼び出しの許可を行う
    - CloudFunctionsの管理画面から各関数にとび、allUsersにcloudfunctions.invokerロールを付与
    - CloudBuildにIAMの管理権限を与えることもできそうだが、はばかられるため
