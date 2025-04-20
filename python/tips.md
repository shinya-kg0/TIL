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



# 継承について

