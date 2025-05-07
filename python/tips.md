# 英単語について
参考ページ
- [モデルやメソッドに名前を付けるときは英語の品詞に気をつけよう](https://qiita.com/jnchito/items/459d58ba652bf4763820)
- [プログラミングでよく使う英単語まとめ](https://qiita.com/Ted-HM/items/7dde25dcffae4cdc7923)

命名するときはある程度正しい英単語を使わないと、ミスリードになってしまうことがある。  
汎用的ではなく意味が直接的なものを選ぶようにする。

# with文使い方
「コンテキストマネージャー」を使うための構文  
例）リソースの管理（ファイル操作、データベース接続、ロック処理など）を安全に行う。

中身の処理は、`__enter__()`,`__exit__()`が定義されているクラスが動いている。


|概念|説明|
|---|---|
|`__enter__()`|with文に入る時の準備（戻り値がasに渡る）|
|`__exit__()`|with文を出る時の後始末（例外処理も行う）|

## 基本の書き方
```py
with open("example.txt", "r") as file:
    content = file.read()
    print(content)
```
with文を使わないで書くと、、、
```py
file = open('example.txt', 'r')
try:
    content = file.read()
finally:
    file.close()  # 閉じ忘れ防止のために必要
```

例外が発生しても、ファイルはちゃんと閉じられる。  

## pytestで使う例
`with pytest.raises(...) `を使うことで例外が発生することを期待する。

```py
import pytest

def divide(a, b):
    return a / b

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```


# 特殊メソッドについて
普通のオブジェクトは組み込み関数が使える。  
例えば、`__len__`などが事前に定義されているので`len(obj)`としても実行できる。

`dir(obj)`で組み込み関数として何が定義されているかがわかる。  
`cls.__class__.__name__`でインスタンス名を取得できる。

ただ、自分で定義するクラスでは自分で組み込み関数を定義しないと使えない、、、  
機械学習モデルを学習させる時のdatasetクラスではindexで中身の値を取り出す必要があるので`__getitem__`を定義する必要がある

```py
class MyList:
    pass

m = MyList()
# print(len(m))  # → TypeError! __len__ がない！
```

次のように定義すれば使える！
```py
class MyData:
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

>>> d = MyData([5,3,2,8])
>>> len(d)

    # d.__len__()でも呼び出せる
```

# リンター、フォーマッター
Pythonにはコードの規約がいろいろあるが、補助ツールとしてflake8,Blackが使える。

## flake8（リンター）
Pythonソースコードの論理エラーやスタイルをチェックする。

修正した方がいい場所と内容は教えてくれるけど、修正自体はしてくれない。

## Black（フォーマッター）
空白や引用符などを自動で変更してくれる。差分も確認できる。  

変更したら、元に戻せないのでGit管理をしておくのがいい。

一部、修正してほしくない場所は次のようにして管理できる。

```py
a = [1,2,3,4]

def hogehoge():
    pass

# fmt: off 
KEY = 'test'
# fmt: on
```

# 単要素のタプルにコンマが必要な理由
インデックスでアクセスしたければコンマが必要。  
もし使わないなら、その文字の何番目かが出力

```bash
>>> a = ("cat")
>>> a[0]
'c'
>>> b = ("cat",)
>>> b[0]
'cat'
```
```bash
>>> c = (3456)
>>> c
3456
>>> c[0]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'int' object is not subscriptable
>>> c = (3456,)
>>> c
(3456,)
>>> c[0]
3456
```

# 継承について
参考ページ
- [初学者のためのPython講座　オブジェクト指向編5　クラスの継承](https://qiita.com/kotakahe/items/b678250389af7fa885a5)

## クラスの継承
クラスの継承を行うことで、親クラスのメソッドを使えるようになる。  
Attrもそのまま使える。（インスタンス化する時に値を渡す必要がある）

```py

# 親クラスを定義する
class Human:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def status(self):
        print("氏名：" + self.name, "年齢：" + str(self.age) + "歳")

# 親クラスを継承した子クラスを定義する
class Human_say(Human):
    def introduce_myself(self):
        print("私は" + self.name + "です。" + str(self.age) + "歳です。")

# 子クラスのインスタンスを生成する
a_man = Human_say("荒木", 58)
# 親クラスのメソッドを呼び出す
a_man.status()
# 子クラスのメソッドを呼び出す
a_man.introduce_myself()

```

## メソッドのオーバーライド

クラスによってメソッドの挙動を変えたい場合はオーバーライドができる。  
同じ名前のメソッドを改めて定義し直せば、親クラスのメソッドではなく子クラスだけのメソッドが使える。

```py
class Human:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def status(self):
        print("氏名：" + self.name, "年齢：" + str(self.age) + "歳")

class English_Human(Human):
    # status()メソッドをオーバーライドする
    def status(self):
        print("NAME：" + self.name, "AGE：" + str(self.age))

# 親クラスのインスタンスを生成する
a_man = Human("荒木", 58)
# 子クラスのインスタンスを生成する
a_eng_man = English_Human("Araki", 58)
# メソッドを呼び出す
a_man.status()
a_eng_man.status()
```

## 親クラスのメソッドを参照
`super()`からメソッドを呼び出すと親クラスのメソッドが使える。

例えば、初期化処理を改めて書かなくて済む（追加する分だけ記述すればいい）

```py
class Human:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def status(self):
        print("氏名：" + self.name, "年齢：" + str(self.age) + "歳")

class Human2(Human):
    # 初期化メソッドをオーバーライドする
    def __init__(self, name, age, blood, job):
        # 親クラスの初期化メソッドを参照する
        super().__init__(name,age)
        # 変数を追加する
        self.blood = blood
        self.job = job
    # status()メソッドをオーバーライドする
    def status(self):
        # 親クラスのstatus()メソッドを参照する
        super().status()
        # status()メソッドに追加する
        print("血液型：" + self.blood,"職業：" + self.job)

a_man = Human2("荒木", 58, "B", "漫画家")
a_man.status()

```

# 属性をプロパティにする（getter, setterの設定）

データの内部構造を隠しつつ、柔軟なインターフェースを提供できる。

例えば、金額やパスワード、日付などのバリデーションが必要な値を扱う時

```py
class Wallet:
    def __init__(self):
        self._bills = []
    
    @property
    def money(self):
        """財布の合計金額を返す(getterの役割)"""
        return sum(self._bills)
    
    @money.setter
    def money(self, bills):
        """
        お札のリストをセット（2000円札は禁止）(自然と0以上を制限している)
        例: wallet.money = [1000, 1000, 10000, 5000]
        """
        if not all(bill in [1000, 5000, 10000] for bill in bills):
            raise ValueError("使えるのは 1000円、5000円、10000円札だけです（2000円札禁止）")
        self._bills = bills
    
    @money.deleter
    def money(self):
        self._bills.clear()
    

if __name__ == "__main__":
    
    wallet = Wallet()
    
    # お札をセット
    wallet.money = [1000, 1000, 5000, 10000]
    
    print(wallet.money)
    
    # 財布を空にする
    del wallet.money
    print(wallet.money)  # → 0
    
    # 2000円札を入れようとするとエラー
    try:
        wallet.money = [1000, 2000]
    except ValueError as e:
        # ValueError: 使えるのは 1000円、5000円、10000円札だけです（2000円札禁止）
        print(e)
```

## デコレーターの説明
|デコレーター|説明|
|---|---|
|@property|読み取り専用の属性を定義（wallet.money）|
|@money.setter|属性に代入した時の動作（wallet.money = [...]）|
|@money.deleter|del wallet.moneyで実行される処理|

# シェルスクリプトとMakefile
|比較項目|シェルスクリプト|Makefile|
|---|---|---|
|目的|手順の自動化<br>初期セットアップや複雑な処理|主にビルドの自動化（依存関係の管理）<br>定型タスク|
|使用される言語|bash, zshなどのシェル言語|makeコマンド用の独自構文|
|ファイル名の例|deploy.sh, setup.sh|Makefile|
|実行方法|bash script.sh, ./script.sh|make, make ターゲット名|
|向いている処理|サーバー設定、ファイル操作、スクリプト全般|ソースコードのビルド、複数ファイルの依存処理|

**依存関係の管理とは、「何を変えたら何を作り直すべきか」を把握して、効率よく再処理するための仕組み。**

## シェルスクリプト
  - **使い道：処理を順番に自動実行する**
  - 上から順に実行
  - 毎回全て実行
  - 柔軟性は高い（何でもかける）

```bash
#!/bin/bash
echo "Python環境のセットアップを始めます..."

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
echo "セットアップ完了！"
```

### よくある用途
- 環境構築
- デプロイ作業
- ローカルテスト一式の実行
- 複数のコマンドをまとめて実行

## Makefile
  - 使い道：「目的ごとにタスクを定義」して、簡単に再実行できるようにする
  - 依存関係に基づいて処理
  - 差分だけ実行（変更ファイルのみ）
  - 処理は限定的（ビルド処理向け）

```makefile
# 仮想環境の作成
venv:
	python3 -m venv venv

# パッケージのインストール
install:
	source venv/bin/activate && pip install -r requirements.txt

# テスト実行
test:
	source venv/bin/activate && pytest tests/

# コード整形チェック
lint:
	flake8 src/

# 全部一括実行
all: venv install lint test
```

### よくある用途
- 依存関係のインストール
- テストの実行
- コードチェック
- 一連の作業


# ループや条件分岐に使う命令集

| 命令         | 主な用途                              | 説明・使い方の例                                                  | 備考                          |
|--------------|---------------------------------------|-------------------------------------------------------------------|-------------------------------|
| `continue`   | 現在のループ処理をスキップ           | 条件に合ったらそのループ回を飛ばし、次の繰り返しへ               | `for` / `while`内で使用       |
| `break`      | ループを途中で終了                   | 目的の値が見つかったらループを即終了                             | `for` / `while`内で使用       |
| `pass`       | 何もしない（空の文）                 | 処理を書く場所の仮置き、`except`などのブロックを空で保つとき     | 影響なし、エラー防止などに    |
| `return`     | 関数を途中で終了し、値を返す         | 条件により処理を終えたり、結果を返す                              | 関数内でのみ使用可能           |
| `else` (ループ)| ループが `break` されなかったときに実行 | すべて確認できたことを示す処理などに                              | `for` / `while`に付けて使う   |
| `try` / `except` | エラーを検知して特別な処理を行う     | 例外が起きたときに処理を切り替える                                | `pass`と一緒に使うことも多い  |
| `assert`     | 条件が成り立たない場合にエラーを出す | デバッグ用。プログラムが想定通り動いているか確認する              | 条件が`False`なら強制終了     |

## continue

```py
# continue の例
for i in range(5):
    if i == 2:
        continue  # i が 2 のときだけスキップ
    print(i)

# 出力
# 0, 1, 3, 4
```

## pass

```py
# pass の例 
for i in range(5):
    if i == 2:
        pass  # ここで何か処理を書く予定だったけど今は空のまま
    print(i)

# 出力
# 0, 1, 2, 3, 4
```

## break
```py
# break の例
for i in range(5):
    if i == 2:
        break  # i が 2 になったらループ終了
    print(i)

# 出力
# 0, 1
```
