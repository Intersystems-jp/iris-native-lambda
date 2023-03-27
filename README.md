# PythonからNativeAPIを利用してIRISに接続する AWS Lambda関数を作成するまでの流れ

AWS Lambda 関数からIRISのNativeAPIを利用して、PythonからIRISに接続するまでの流れをご紹介します。

※ 事前にAWSのEC2インスタンス（Ubuntu 20.04を選択）にIRISをインストールした環境を用意した状態からの例でご紹介します。

なお、AWS Lambda関数のレイヤー作成、関数作成の流れは、開発者コミュニティの記事：[PyODBC経由でIRISに接続するAWS Lambda関数を作成するまでの流れ](https://jp.community.intersystems.com/node/538541) と同様のため、このリポジトリの説明では割愛しています。詳細な流れは記事をご参照ください。

以下の内容をご紹介します。

1. [Native API レイヤー用Zipの作成](#1-native-api-レイヤー用zipの作成)
2. [サンプルのクラス定義のインポート](#2サンプルのクラス定義のインポート)
3. [関数の作成とテスト実行](#3-関数の作成とテスト実行)
4. [Cloudformatio___nのYAML例](#4-cloudformationのyaml例)
___

## 1. Native API レイヤー用Zipの作成

Native API用モジュールのレイヤーを以下の手順で作成します。
```
wget https://github.com/intersystems/quickstarts-python/raw/master/Solutions/nativeAPI_wheel/irisnative-1.0.0-cp34-abi3-linux_x86_64.whl
unzip irisnative-1.0.0-cp34-abi3-linux_x86_64.whl
cd ..
zip -r9 ../iris_native_lambda.zip *
```

この流れで作成したZipの例：[iris_native_lambda.zip](iris_native_lambda.zip)

## 2.サンプルのクラス定義のインポート

Native APIでは、IRIS内のメソッドやルーチンを実行できます。

サンプルとして、[Test.Utils](/examples/Test/Utils.cls)クラスを用意しています。サンプルコード：[index.py](/examples/index.py)を試す場合は事前にインポートしてください。

インポートは管理ポータルから、またはVSCodeから、または[Utils.cls](/examples/Test/Utils.cls)をIRISをインストールした環境に転送後、ユーティリティからインポートすることができます。

- 管理ポータルからインポートする場合

    `http://IPアドレス:52773/csp/sys/UtilHome.csp` にアクセスし、**システムエクスプローラ→クラス→ネームスペース：USER→インポートボタン** をクリックします。

    [Utils.cls](/examples/Test/Utils.cls)をファイルに指定してインポートを行ってください。

    ![](/assets/mp-import.png)

- VSCodeを利用する場合

    VSCodeにObjectScriptエクステンションをインストール後、IRISに接続し[Utils.cls](/examples/Test/Utils.cls)保存します（Ctrl+S）。

    >詳細は [VSCode を使ってみよう！](https://jp.community.intersystems.com/node/482976)をご参照ください。

- [Utils.cls](/examples/Test/Utils.cls)をIRISをインストールした環境に転送後、ユーティリティからインポートする

    [Utils.cls](/examples/Test/Utils.cls) を `/usr/irissys/mgr/user` ディレクトリに配置した状態での実行例です。

    IRISにログインします（USERネームスペースにログインしています）。
    ```
    iris session IRIS
    ```
    インポート用ユーティリティを利用してインポートを実施します。
    ```
    do $system.OBJ.Load("/usr/irissys/mgr/user/Utils.cls","ck")
    ```

    実行例は以下の通りです。
    ```
    USER>do $system.OBJ.Load("/usr/irissys/mgr/user/Utils.cls","ck")

    Load started on 03/27/2023 09:36:21
    Loading file /usr/irissys/mgr/user/Utils.cls as udl
    Compiling class Test.Utils
    Compiling routine Test.Utils.1
    Load finished successfully.

    USER>    
    ```

## 3. 関数の作成とテスト実行

レイヤー用Zip：[iris_native_lambda.zip](/iris_native_lambda.zip)と、サンプルコードの[index.py](/examples/index.py)と[connection.config](/examples/connection.config)をZipにしたファイル：[iris_native_code.zip](/iris_native_code.zip)を利用してAWS Lambda関数を作成します。

作成とテスト実行の流れついては、開発者コミュニティの記事：[PyODBC経由でIRISに接続するAWS Lambda関数を作成するまでの流れ](https://jp.community.intersystems.com/node/538541#createLayer)以降をご参照ください。

### 確認：IRISへの接続情報について
サンプルのpythonスクリプト：[index.py](/examples/index.py) では、以下いずれかの方法でIRISに接続できるように記述しています。

環境変数を使用する index.pyには、lambda関数作成時に設定する環境変数を利用するように記述しています（19～23行目） 。なお、環境変数は、Lambda関数登録後、画面で追加／変更できます。

[connection.config](/examples/connection.config) を使用する index.py の10行目と12～16行目のコメントを外し19～23行目をコメント化して利用します。 接続するIRISの情報に合わせて [connection.config](/examples/connection.config) を変更してください。


### テスト実行の引数例

※引数に指定するJSONプロパティに値の指定がない場合は、"**none**"を指定してください。

- TestlUtilsクラスのHello()メソッドを実行する場合の引数例
    ```
    {
        "method": "Hello",
        "function":"none",
        "args": "none"
    }
    ```
    以下の戻り値が返ります。
    ```
    "{\"message\":\"こんにちは！今の時間は：2023年3月27日 10:16:05です\",\"status\":1,\"payload\":\"IRIS for UNIX (Ubuntu Server 20.04 LTS for x86-64) 2022.1.2 (Build 574U) Fri Jan 13 2023 15:03:40 EST\"}"
    ```

-  Test.Personテーブルの作成とダミーデータの登録する場合の引数例

    TestlUtilsクラスのCreateDummyTbl()メソッドを実行する場合
    ```
    {
        "method": "CreateDummyTbl",
        "function":"none",      
        "args": "none"
    }
    ```
    以下の戻り値が返ります。

    ```
    "{\"Message\":\"登録完了\"}"
    ```


- Test.PersonテーブルのSELECTの結果を取得する場合の引数例

    Test.UtilsクラスのGetPetPerson()メソッド実行する場合
    ```
    {
        "method": "GetPerson",
        "function":"none",
        "args": "none"
    }
    ```
    以下の戻り値が返ります。
    ```
    "[{\"Name\":\"山田\",\"Email\":\"taro@mail.com\"},{\"Name\":\"斉藤\",\"Email\":\"saito@mail.com\"}]"
    ```

- ^KIONグローバル変数を設定する例
    
    Test.UtilsクラスのCreateDummyGlo()メソッドを実行する場合の引数例
    ```
    {
        "method": "CreateDummyGlo",
        "function":"none",
        "args": "none"
    }
    ```
    以下の戻り値が返ります。
    ```
    "{\"Message\":\"登録完了\"}"
    ```

- index.pyのFunctionを動かす例

    ^KION全データ取得する get_globaldata()関数を実行する例
    ```
    {
        "method":"none",
        "function":"getglobal",
        "args":"none"
    }
    ```

    以下の戻り値が返ります。
    ```
    "[[\"久留米\", 14, 19], [\"大阪\", 12, 18], [\"奈良\", 10, 18], [\"愛知\", 13, 15], [\"新潟\", 6, 12], [\"東京\", 14, 19], [\"沖縄\", 21, 26]]"
    ```

- index.pyのFunctionを動かす例

    ^KIONにデータを追加する場合の引数例
    ```
    {
        "method":"none",
        "function": "setglobal",
        "args": {"area":"長野","min":5,"max":10}
    }
    ```
    正しくデータ登録できたかどうかは、get_globaldata()関数を再度実行すると確認できます。
    
    以下、get_globaldata()関数を再実行した場合の戻り値の例です。
    ```
    "[[\"久留米\", 14, 19], [\"大阪\", 12, 18], [\"奈良\", 10, 18], [\"愛知\", 13, 15], [\"新潟\", 6, 12], [\"東京\", 14, 19], [\"沖縄\", 21, 26], [\"長野\", 5, 10]]"
    ```

## 4. CloudformationのYAML例

例：[cloudformation.yml](/cloudformation.yml)

実行の流れについては、「[PyODBC経由でIRISに接続するAWS Lambda関数を作成するまでの流れ]の」[3. 1,2の流れをCloudformationで行う例](https://jp.community.intersystems.com/node/538541#Cloudformation)と同様です。
