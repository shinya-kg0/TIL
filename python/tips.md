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


# Enumの使い方

Enumとは、「**選択肢が決まっている値に名前をつけて安全に扱う仕組み**」

例えば、
- 注文の状態：未処理 / 処理中 / 配送済み
- ユーザーの権限：一般 / 管理者 / ゲスト
- エラーラベル：INFO / WARNING / ERROR

これらを **数字や文字列で直接管理するより、Enumで明示する**ことで安全で読みやすくなります。

## 基本的な使い方
```py
from enum import Enum

class OrderStatus(Enum):
    PENDING = 1
    PROCESSING = 2
    SHIPPED = 3

# 使い方
status = OrderStatus.PROCESSING

if status == OrderStatus.PROCESSING:
    print("注文は現在処理中です")
```


## Enumの実務利用例

| シーン | 使いどころ | Enum例 |
|--------|-------------|--------|
| 注文管理 | 注文の状態 | `OrderStatus.PENDING` |
| ユーザー管理 | 権限の区別 | `UserRole.ADMIN` |
| バックエンドAPI | HTTPメソッド種別 | `HttpMethod.POST` |
| ログ処理 | ログの重要度 | `LogLevel.WARNING` |
| UI制御 | ボタンの状態 | `ButtonState.DISABLED` |

## Enumのメリットまとめ

| メリット | 説明 |
|----------|------|
| ✅ **意味が明確になる** | `status == OrderStatus.SHIPPED` のように、意図が明らかになる |
| ✅ **間違った値を防げる** | `"SHIPPED"` など文字列比較ではなく、正しい選択肢しか使えない |
| ✅ **保守性が高い** | 値を後から変更しても、名前でコードを書いていれば影響が少ない |
| ✅ **IDE補完が効く** | VSCodeなどで `.SHIPPED` の候補が出る |
| ✅ **ループ処理や比較が簡単** | 全パターンを `for status in OrderStatus:` で扱える |

💡 他にもif文の比較などで数値を使うと早く処理できるので、Enumを使って**可読性と処理の速さを向上**できる。


## Enumの注意点・デメリット

| 注意点 | 解説 |
|--------|------|
| ❌ **値そのもの（数値/文字列）と直接比較できない** | `status == "SHIPPED"` はNG、正しくは `status == OrderStatus.SHIPPED` |
| ❌ **Enumの `.value` に依存すると保守性が下がる** | 値より名前を使うことを意識 |
| ❌ **JSONへの変換が一手間かかる** | Enumはそのままだと `JSON` にシリアライズできない（カスタム処理が必要） |

PythonのEnumは、  
「決められた選択肢に名前を与えて、安全に・分かりやすく使う仕組み」です。  

# パッチ処理について
pytestだと`monkeypatch`、汎用的なものだと`textfixtures.replace`が使える！

細かい使い方はノート6月に記載

## monkeypatch

```py
@pytest.fixture
def patch_hoge(monkeypatch):
    def dummy(*args):
        return True
    monkeypatch.setattr(target, attr, dummy)

def test_hogehoge(patch_hoge):
    pass
```

## textfixtures.replace

```py
from textfixtures import replace

def patch_hoge(*args):
    return True

@replace('target_func', patch_hoge)
def test_hogehoge():
    pass
```


# ジェネレータ

「一度に全部ではなく、必要な分だけ順番に値を返す仕組み」

普通のリストだと、全ての要素をメモリ上に展開する。
```py
nums = [x for x in range(1000000)]  # 全要素を作成
```
逆にジェネレータだと、必要になった時に次の値を生成する。（遅延評価という）  
→ メモリ効率が非常に良い

## ジェネレータの作り方

- 関数の中で`yield`を使うと、ジェネレータ関数になる。

```py
def count_up_to(n):
    count = 1
    while count <= n:
        yield count   # 値を返すが、関数は終了しない
        count += 1

gen = count_up_to(3)
print(next(gen))  # 1
print(next(gen))  # 2
print(next(gen))  # 3
```

yield は return と違って、**途中で処理を止めて次回再開できる**のがポイント  
→ ステート（状態）を持てる


## ジェネレータ式

リスト内包表記的な感じで、丸括弧を使うとジェネレータ式になる

```py
gen = (x * x for x in range(5))  # 0〜4の2乗を順に返す

print(next(gen))  # 0
print(next(gen))  # 1
print(next(gen))  # 4

for value in gen:  # 残りを順に取り出す
    print(value)   # 9, 16
```

## 活用できる場面

- 大量データの処理（ログ解析、CSVストリーム処理など）
- 無限列の生成（例: 自然数、フィボナッチ数列）
- ファイルやネットワークからの逐次読み込み

### 具体例

#### 大容量ファイルの読み込み

CSVやログファイルなど、GB単位のデータを処理する時にジェネレータは必須。

- 全行をリスト化せず、1行ずつ読み込むのでメモリ効率が良い。
- ログ解析やストリーミングデータ処理で超よく使うパターン。

```py
def read_large_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:     # ファイルオブジェクト自体がジェネレータ
            yield line.strip()

for row in read_large_file("access.log"):
    # メモリに全行を載せずに1行ずつ処理
    process(row)
```



#### Web APIのページネーション

APIが1リクエストあたり100件しか返さない場合、ジェネレータで順次取得。

- 無限に近いページ数でも、使う分だけ順次取得。
- バッチ処理やスクレイピングでかなり多用。

```py
import requests

def fetch_users():
    page = 1
    while True:
        res = requests.get(f"https://example.com/api/users?page={page}")
        data = res.json()
        if not data["users"]:
            break
        for user in data["users"]:
            yield user
        page += 1

for user in fetch_users():
    save_to_db(user)
```

#### PyTorchのDataset & DataLoader

PyTorchではDatasetがジェネレータ的役割を果たします。

```py
from torch.utils.data import Dataset, DataLoader
import torch

class MyDataset(Dataset):
    def __init__(self, file_paths):
        self.file_paths = file_paths

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, idx):
        x = torch.randn(3,224,224)  # 画像読み込み
        y = torch.randint(0,2,(1,)) # ラベル
        return x, y

dataset = MyDataset(file_paths=["a","b","c"])
loader = DataLoader(dataset, batch_size=32, shuffle=True)

for x_batch, y_batch in loader:
    # バッチ単位で順次ロード
    pass
```

- DataLoader内部はイテレータ（ジェネレータ）で動いている。
- GPUメモリに入りきらないデータでも問題なく扱える。

#### 推論パイプラインで逐次実行

学習済みモデルに対して、膨大なデータを推論させる場合もジェネレータが便利です。

```py
def predict_in_batches(model, data_stream, batch_size=64):
    batch = []
    for sample in data_stream:
        batch.append(sample)
        if len(batch) == batch_size:
            yield model.predict(batch)
            batch.clear()
    if batch:
        yield model.predict(batch)
```

- 推論も一気にではなく、バッチ単位で分割可能。
- サーバー推論やバッチ推論の効率化に使う。


# クロージャ

Pythonでいうクロージャは、関数が定義されたときのスコープ（変数の状態）を保持したまま、外側の関数が終了しても使える関数。

→ イメージは「外の変数を持ち歩く関数」

```py
def outer_function(x):
    def inner_function(y):
        return x + y  # outer_functionのxを覚えている
    return inner_function

adder_5 = outer_function(5)
print(adder_5(10))  # 15
print(adder_5(3))   # 8
```

- outer_function が終了しても x=5 が記憶されている
- adder_5 は「5を加算する関数」として動く

## よく使う場面

### デコレータ

Pythonのデコレータは内部的にクロージャを利用しています。

例：ログ出力デコレータ

```py
def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_decorator
def process_data(data):
    return data * 2

process_data(10)  # Calling process_data
```

- wrapper が log_decorator のスコープを保持
- 実務ではログ出力、認証、キャッシュ制御、リトライ処理などで多用


### 設定値や状態を持つ関数

外部変数をグローバルに置きたくない場合、クロージャでカプセル化します。

```py
def multiplier_factory(factor):
    def multiplier(value):
        return value * factor
    return multiplier

double = multiplier_factory(2)
triple = multiplier_factory(3)

print(double(5))  # 10
print(triple(5))  # 15
```

- 同じロジックで係数だけ変える処理などに便利
- 設定値が変数として「隠れる」のでグローバルを汚さない

### 機械学習パイプラインの前処理

クロージャで前処理関数を生成して、状態（標準化の平均・分散など）を保持できます。

```py
def standardizer(mean, std):
    def transform(x):
        return (x - mean) / std
    return transform

std_transform = standardizer(mean=100, std=15)
print(std_transform(115))  # 1.0
```

- データ前処理パラメータをクロージャに持たせる
- モデルの推論時も同じ変換を再利用できる

## キャッシュ関数（メモ化）

外部変数を保持して関数呼び出しを高速化。

```py
def memoize():
    cache = {}
    def wrapper(x):
        if x not in cache:
            cache[x] = x ** 2
        return cache[x]
    return wrapper

square = memoize()
print(square(4))  # 計算
print(square(4))  # キャッシュから
```

- 同じ計算を何度もせずに済む
- 数値計算や機械学習の前処理高速化に使える

