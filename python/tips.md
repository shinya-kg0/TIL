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

# 継承について

