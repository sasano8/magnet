# ymltree
treeコマンドの出力結果をymlとして出力するためのライブラリです。

# Why
treeコマンドは、ディレクトリ構造を人の目で見て直感的に分かりやすい形で出力しますが、その出力は再利用を考慮されていません。時々、テキストにディレクトリ構造を定義し、定義からディレクトリを自動生成したいと考えることはありませんか？このライブラリは、ymlでディレクトリ構造をシリアライズし、他社がそれをデシリアライズすることを支援します。

# Getting Started

```
ymltree
ymltree --output directories.yml
ymltree --make diretories.yml
```
