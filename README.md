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


