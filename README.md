# magnet
様々な実験的な機能を含むデータ収集・データ分析・仮想通貨等の自動売買を目指す。

# functions
- crawler
  - crypt currency
- etl
- job manager & message queue
- data store
- full text search(backend: elasticsearch)
- auto trading

# awasome python packages

- [python cheet sheet](https://github.com/crazyguitar/pysheeet/blob/master/docs/notes/python-sqlalchemy.rst)
- [tree構造とかのライブラリ?](https://github.com/dahlia/awesome-sqlalchemy)
- [html本文を抽出 1.5万](https://github.com/buriy/python-readability)
- [htmlをオブジェクト化自然言語処理 1.5万](https://github.com/codelucas/newspaper)
- [強力なWEBスパイダー 14万](https://github.com/binux/pyspider)
- [強力なWEBスパイダー 14万](https://github.com/binux/pyspider)
- [クラス定義デコレータ化 3.2万](https://github.com/python-attrs/attrs) pydanticの前身みたいなもん


# test
```
pytest --cov -v -s
```

# 開発環境構築
```

# 1. 開発環境のUID/GIDを確認する
cat /etc/passwd
# <username>>:x:<uid>:<gid>:,,,

# 2. .envにuid gidを記述する（開発時に、ホストOSとコンテナ内のユーザをバインドし、権限エラーが生じないようにする）
vi .env

# 3. dockerコンテナを起動する
docker-copmpose up -d --build

```

# バックエンド

## コマンドラインユーティリティ
```
python3 -m cli
```

## データベース初期化
```
python3 -m cli db migrate
```

## データベースマイグレーション
```
python3 -m cli db makemigrations
python3 -m cli db migrate
```


# 売買アルゴリズム

- エントリーサイン
- 利確サイン

## クロス（ゴールデンクロス・デッドクロス）
ゴールデンクロス・デッドクロステクニカルを用いた売買を、仮想通貨ペアbtcjpyで検証した。
ゴールデンクロス・デッドクロステクニカルの判定は、単純移動平均線（５日）が単純移動平均線（２５日）を上回る、もしくは、下回るタイミングとする。

- ペア： btcjpy
- 期間： 2018/1/7 〜 2020/9/28
- エントリー： ゴールデンクロスで買・利確　デッドクロスで空売・利確のドテン方式とした。
　　　　　　ビットコインの上昇トレンド中は損益率が良すぎるため、ビットコインが再高値をつけた後のデッドクロスを初回エントリーとした。
- 確定： 次回クロス発生時（指値でなくサインによる確定）
- 数量： 1ビットコイン固定(初エントリ時1996140円)
- 勝率： 43%
- レンジ：1996140　〜　1138923
- 損益： 1531141
- 平均損益：　35000円(100万円 3.5%)
- 回転率： 月1.5回程度
- 所見： 最大の利益を狙うのでなく、ゆるやかな利益を狙う。
天井・底打ちの大きなトレンド転換時に利益を上げられず、遅れて反応する。
そのようなリバウンド等、強い抵抗がある相場を苦手としているように思える。
方向性が分からない相場で勝っている。
連続して負けた後は、負けをチャラにするような勝ち方をする。
中期レンジ相場で機能しているように見える。
ボリュームとはあまり因果関係がないように見える。
最大の利益が取れないアルゴリズムのため、利確タイミングを改善するだけで大きく成果を上げられそうだ。
大きく利幅を取った後は、負けることが多い。（利幅1.4％目安）
短期的な暴騰・急落に弱そうで、時価総額が低いアセットなど単一意思の資金注入の影響を受けやすいため、トレンドが働かない。
買いと売りでどちらが利益率が高いのか調べたところ、売りの方が利益を上げていた。
と思ったが、2017年末に最高値をつけ、激しい値動きで損失を出していた。
このように短期間に激しく動くような相場で相性が悪い。

そのため、トレンド感がないレンジ相場対応と、激しく殴り合っている爆弾相場に対応するアルゴリズムで弱点を補いたい。
あと、リミットは1.4倍におく
小さい負けが多いのでレンジで補完する。
トレンド用スロット
レンジ用スロット
有事用スロット
がいる

次のアルゴリズムは
クロスで逆にエントリーし、
1.1%で利確
サイン検出で反転
0.9%で損切り
両建でリスクヘッジしつつ、トレンドアルゴリズムのウィークポイントをカバーする
損切りしたとしても、その後は大きく伸びる傾向があるので取り戻せる



# 開発ガイドライン

## データベース/トランザクション
当該アプリケーションでトランザクションを扱う場合は、リポジトリを介して操作を行ってください。
リポジトリは暗黙的なコミットを行いませんが、要所でflush（データベースにSQLを発行）を行い、id等が発行されたオブジェクトを返します。
それらは、セッションがスコープを抜けた際に、自動的にcommitされ永続化されるか、例外発生時に自動的にrollbackされます。
これにより、様々なレコード操作処理を一連のトランザクションとして組み合わせることができます。
以下はサンプルコードです。
obj1、obj2のレコードの仮作成（flush）は、例外発生によりrollbackされ、一貫性が担保されます。

```
def get_db() -> Iterable[Session]:
    db: Session = CreateSession()
    try:
        yield db
        db.commit()
    finally:
        # noinspection PyBroadException
        try:
            # In case of uncommit, it will be rolled back implicitly
            db.close()
        except Exception as e:
            logger.critical(exc_info=True)

def sample_transaction()
    for db in get_db():
        rep1 = crud.Repository1(db)
        rep2 = crud.Repository2(db)
        obj1 = rep1.create()
        print(obj1.id)  # => 1
        obj2 = rep2.create()
        print(obj2.id)  # => 2
        raise Exception()
    
    return obj1, obj2

sample_transaction()
```

## データベース/バージョンカウンター
データベースのトランザクション分離レベルが"REPEATABLE READ"以下の場合、ある処理を行っている間に別のトランザクションでレコードが更新された場合、
更新が衝突し値が消失する可能性があります。通常、同時更新に対してターゲット行をロックするか、コミット時にエラーを発生させるなど対応が必要になります。
Sqlalchemyでは、version_id_colを用いることで同時実行制御を行うことができます。

- [参考](https://docs.sqlalchemy.org/en/13/orm/versioning.html)



fastapi-realworld-example-appの構成
-----------------

Files related to application are in the ``app`` or ``tests`` directories.
Application parts are:

::

    app
    ├── api              - web related stuff.
    │   ├── dependencies - dependencies for routes definition.
    │   ├── errors       - definition of error handlers.
    │   └── routes       - web routes.
    ├── core             - application configuration, startup events, logging.
    ├── db               - db related stuff.
    │   ├── migrations   - manually written alembic migrations.
    │   └── repositories - all crud stuff.
    ├── models           - pydantic models for this application.
    │   ├── domain       - main models that are used almost everywhere.
    │   └── schemas      - schemas for using in web routes.
    ├── resources        - strings that are used in web responses.
    ├── services         - logic that is not just crud related.
    └── main.py          - FastAPI application creation and configuration.


    magnet
    ├── common        - common component for components.
    ├── componets        - web related stuff.
    │   ├── views(api)             - api
    │   ├── schemas                - validation
    │   ├── repositories(crud)     - crud
    │   ├── models                 - model
    │   ├── query                  - query
    │   ├── events                 - event
    │   ├── utils                  - utils
