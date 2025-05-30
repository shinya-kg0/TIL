# 用語集

## 踏み台サーバーとプロキシサーバーの違いまとめ（GPT編集）

### 🧱 踏み台サーバーとは？

**踏み台サーバー**は、外部から直接アクセスできない内部ネットワーク上のサーバーに対し、  
**安全にアクセスするための中継サーバー**です。

#### ✅ 主な使い道
- 社内やクラウド上の**非公開サーバーにSSH接続**したいとき
- **セキュリティの強化**（アクセス経路を制限・ログ取得）
- 本番環境へのアクセスを制限して、踏み台経由に一本化する

---

### 🌐 プロキシサーバーとは？

**プロキシサーバー**は、ユーザーのリクエストを受け取り、**代わりに外部へ通信する中継サーバー**です。

#### ✅ 主な使い道
- **Webアクセスの監視・制御（フィルタリング）**
- **社内のインターネット利用制限**
- 匿名でWebアクセス（IPマスキングや地域制限の回避）

---

### 🔍 違いを一覧で比較

| 項目 | 踏み台サーバー | プロキシサーバー |
|------|----------------|------------------|
| 📌 主な目的 | 内部サーバーへの安全な接続 | 外部Webへの通信の制御・仲介 |
| 📍 通信の方向 | 外部 → 内部 | 内部 → 外部 |
| 🔐 通信プロトコル | SSH, RDP など | HTTP, HTTPS, FTP など |
| 👤 利用者 | 管理者・開発者 | 一般ユーザー・社員 |
| 📂 主な用途 | サーバー管理、保守作業 | Webアクセス制限、ログ管理 |
| 🧰 使用例 | AWS内のDBへSSH接続 | YouTubeブロック、社外Web制限 |
| 📋 ログ活用 | 誰がどのサーバーにアクセスしたか | 誰がどのWebサイトにアクセスしたか |

---

### 📝 まとめ

- **踏み台サーバー**は「中に入るための門番」
- **プロキシサーバー**は「外に出るときのフィルター」

どちらも「中継」だけど、目的と使い方が大きく違います。

---
## 浅いコピーと深いコピーの違い

### 浅いコピー
- オブジェクトの一番外側の構造だけをコピーする。
- ネストされた要素に関しては元のものと同じものを参照する。

#### 注意点
原則としては、**意図せず他の処理に影響を与えないようにコピーは使う。**  
その上で、単純なリストや辞書などは浅いコピーで十分である。

ただ、十分に注意して使わないとネスト内の処理で意図せずデータが書き換わることがあるので注意！

### 深いコピー
- オブジェクトのすべての階層を再起的にコピーする。
- 中の要素も完全に別物になる。

#### 注意点
テンプレートや設定値を元データを壊さずに使いまわしたい時に有効である。  
多少、浅いコピーの方が処理が楽である。


## makeコマンドとMakefile

コマンドをまとめて管理して、面倒な手打ち作業を効率化できる！

### 具体例
たとえば、Python開発で仮想環境を作って依存パッケージをインストールしてFlake8でコードをチェックしてテストを走らせて、、、

ちょいちょい同じ作業を手打ちしていることがある。  
→ これを効率化できるのが`Makefile`!!

<details><summary>具体例</summary>

```bash
# Makefile

# 仮想環境を作って依存関係をインストール
init:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

# Linterチェック
lint:
	flake8 src

# フォーマット
format:
	black src

# テスト実行
test:
	pytest tests

# 環境を綺麗にする
clean:
	rm -rf build src/*.c src/*.so __pycache__

# 一括で全部やる
all: lint format test
```

実行コマンド
```bash
make init     # 仮想環境＋パッケージインストール
make lint     # コードチェック
make format   # フォーマット（black）
make test     # テスト実行
make          # lint + format + test を全部実行（= all）
```

</details>

### 補足
`Makefile`を書くときの注意点は
- 行頭スペースはタブじゃ無いとダメ
- コマンドが複数あるときは && でつなぐ or 複数行書く
- .PHONY をつけると保険になる（名前の衝突防止）  
`.PHONY: init lint format test all`


## バイパスとは
通常の意味は「混雑を避けるための迂回路」

### ネットワークにおけるバイパス
ネットワーク機器に不具合が生じた場合や何らかの理由でトラブルが起きた時にネットワークを遮断させないように**不具合が発生したシステムを迂回**することで、ネットワーク上の正常動作を維持する機能のこと

### セキュリティにおけるバイパス
OSやアプリに備わっている保護機能を回避されたりセキュリティ対策をすり抜けられてしまうこと。

例）セキュリティ機能をバイパスされる


## スペックアウトとは
「何を作るか」「どう作るのか」を細かく図や文書でまとめること。（仕様を明確にすること）

### 抑えておきたいポイント
- 要求の粒度を揃えることができること
  - **要求分析ツリーを使って目的（理由）と手段（要求）の連鎖によって系統立てて整理**
- 要求の親子関係を把握できること
- 機能間の処理の関係性が把握できること
- 機能間で共有しているデータの関連性が把握できること
  - ロバストネス図を使って機能（静的）と処理、データフロー（動的な側面）をモデル化
- スペックアウト資料を充実させる（二元表、T字マトリクス）
  - モジュールの呼び出し関係を把握できる
  - 調査済み、未調査が把握できる
  - データの読み書きモジュールが簡略にまとめられること

## ターミナルとシェルとは
- ターミナル・・・コンピュータに文字（コマンド）で指示を出すためのアプリ（画面）
- シェル・・・ターミナルで入力したコマンドを実際に処理してくれるプログラム（処理担当）
  - bash, zshなどの種類がある

### シェルスクリプトとは、、、
普通のコマンドは一つだけを実行する命令だが、  
シェルスクリプトは**複数のコマンドを順番にまとめて自動で実行するファイル**
```bash
#!/bin/bash
echo "Hello!"
mkdir my_folder
cd my_folder
touch readme.txt
```

## カーネルとは
- カーネル
  - OSの心臓部
  - コンピュータのリソース（CPU、メモリ、ディスク）を管理・制御している

カーネルに直接指示を出すことはできない。  
シェルを使って抽象的なコマンドを渡して、それをカーネルが解釈し、ハードウェアを制御して出力する

|項目|シェル|カーネル|
|---|---|---|
|役割|ユーザーの命令を受け取り、カーネルに伝える|コンピュータを動かす中枢。命令を実行する|
|誰とやりとりする？|ユーザーとカーネルの仲介|シェルやアプリからの命令を処理|
|例えると|ウェイター（注文を聞く）|シェフ（実際に料理を作る）|
|表から見える？|画面に見える（ターミナル上で使う）|見えない（OSの内部で動く）|
|ユーザーが操作する？|できる（コマンド）|できない|

## 関数とメソッドの違い
- 関数
  - `def hogehoge():`で定義され、いつでも呼び出せる
- メソッド
  - クラス内で定義して、インスタンス経由で呼び出す
  - `obj.method()`で呼び出す。

## モジュールとパッケージの違い
- モジュール
  - Pythonのファイル1つで、機能のまとまり
- パッケージ
  - モジュールをまとめたフォルダ
  - `__init__.py`がある

## クラスとインスタンスの違い
- クラス
  - 設計図
  - どんな要素を持っていて、どんな機能がある？などを定義する
- インスタンス
  - クラスから実体として作ったもの
  - クラスの定義に沿ってそれぞれ生み出したもの

## リストとタプルの違い
- リスト
  - `[1, 2, 3]`
  - ミュータブル（変更可能）
  - 要素の追加などができる（`.append()`）
  - 後で中身をいじる時などに有効
  - やや遅いが柔軟性が高い
- タプル
  - `(1, 2, 3)`
  - イミュータブル（変更不可）
  - 変更操作がそもそもできない、、、
  - 中身を固定したい時に有効
  - 引数や戻り値についてはタプルを使った方がいい
