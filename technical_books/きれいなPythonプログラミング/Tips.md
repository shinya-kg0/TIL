## path操作について

Pythonのpath操作にはpathlibモジュールが使える。  
Pathオブジェクトが生成される。

```py
from pathlib import Path

# ホームディレクトリ
Path.home()

# カレントディレクトリ
Path.cwd()
```

### 基本的な使い方について
1. Pathオブジェクトの作成
    ```py
    from pathlib import Path

    p = Path('/path/to/file.txt')
    ```
    文字列ではなく、オブジェクト指向的にパスを扱える。

2. ファイル・ディレクトリの存在確認
    ```py
    p.exists()      # ファイル・ディレクトリが存在するか
    p.is_file()     # ファイルかどうか
    p.is_dir()      # ディレクトリかどうか
    ```
    ファイル操作前に必ず確認するべき。

3. ファイル名・拡張子の取得
    ```py
    p.name        # 'file.txt'
    p.stem        # 'file'（拡張子なし）
    p.suffix      # '.txt'
    p.parent      # '/path/to'
    ```
    データ処理・ログ整理などでめちゃくちゃ使う。

4. ファイル・ディレクトリの作成
    ```py
    p.mkdir(parents=True, exist_ok=True)  # 階層も含めてディレクトリ作成
    (p / 'subdir').mkdir(exist_ok=True)
    ```
    出力用のディレクトリを作ったりするときに必要

5. パスの結合
    ```py
    new_path = p / 'subdir' / 'newfile.txt'
    ```

6. 特定ファイルの取得
    ```py
    path = Path('./diary')
    file_lst = []
    for file in path.glob('*.md'):
        file_lst.append(file.stem)
    ```
    `path.glob`を使って取得する

    **補足**：`path.rglob`を使うとサブディレクトリ内も全て再帰的に検索する。


## プログラムとプロセスについて

### プログラムとは
「**コンピュータにやってほしいことを、順番に書いた命令書**」

コンピュータは丁寧に指示を与えないと想定通りに動いてくれない。  
→ 細かく指示してあげる必要がある。

例えば、初めにこのファイルを開いて、このデータとこのデータを集計して、ファイルに出力するなど、、、

### プログラムを実行するには

ターミナルで実行することを想定する。  
実行する方法は2種類ある。

- 実行したいファイルがあるディレクトリまで移動してファイル名を実行
- 任意のディレクトリで実行したいファイルのフルパスを実行
  - もし環境変数にそのファイルが入っているディレクトリが設定されていれば、ファイル名だけでOK


### プロセスとは
「**実際に動いているプログラム**」

各プロセルは独立に動作している。コンピュータはいろいろなプロセスを同時に動かしている！  
（wordとchromeを同時に使っている）

プロセスとして実行するには**CPUとメモリを割り当てる**ことが必要！

OSには次の状況を考慮して割り当てをリアルタイムで調整している。
- 今プロセスがどんな状態か（動いているか、止まっているか）
- どのプロセスがどれぐらい重要か（優先度）
- どれぐらい長く動かしたか（平等か）

#### プロセスを確認したい時は、、、
- windowsの場合・・・`Ctrl + Shift + Esc`でタスクマネージャー起動
- macの場合・・・アクティビティモニタで確認
- linuxの場合・・・`Ctrl + Shift + Delete`でタスクマネージャー起動


## よく使うコマンドについて

### find
- findコマンド使い方
  - `find . -name "*.txt"`
  - zshの代替案：`ls ./**/*.txt`、**をつけることで階層を降りることができる。

### where
プログラムが配置されている場所がわかる。

### 環境変数
環境変数は、OSやアプリケーションが動作する際の設定や情報を保存・参照するための仕組みであり、プログラムの挙動や動作環境を柔軟に制御するために不可欠なもの。

winなら`set`、mac,linuxなら`env`で環境変数を確認できる。

## Pythonicな書き方

### 条件分岐と値の設定
```py
# ❌ 非Pythonic
if x is not None:
    y = x
else:
    y = 10

# ✅ Pythonic
y = x if x is not None else 10
```

###  ループとリスト操作（リスト内包表記）
```py
# ❌ 非Pythonic
result = []
for i in range(10):
    result.append(i * 2)

# ✅ Pythonic
result = [i * 2 for i in range(10)]
```

### 辞書アクセス時のデフォルト値

```py
# ❌ 非Pythonic
if 'key' in data:
    value = data['key']
else:
    value = 'default'

# ✅ Pythonic
value = data.get('key', 'default')
```

### 変数値のスワップ
```py
# ❌ 非Pythonic
temp = a
a = b
b = temp

# ✅ Pythonic
a, b = b, a
```

### 条件による早期リターン
```py
# ❌ 非Pythonic
def process(data):
    if data:
        # 処理
        ...

# ✅ Pythonic
def process(data):
    if not data:
        return
    # 処理
    ...
```

### Truthy / Falsy の活用
```py
# ❌ 非Pythonic
if len(my_list) > 0:
    ...

# ✅ Pythonic
if my_list:
    ...
```

### 複数の値との比較
```py
# ❌ 非Pythonic
if fruit == 'apple' or fruit == 'orange' or fruit == 'banana':
    ...

# ✅ Pythonic
if fruit in {'apple', 'orange', 'banana'}:
    ...
```

### enumerate の活用
```py
# ❌ 非Pythonic
for i in range(len(items)):
    print(i, items[i])

# ✅ Pythonic
for i, item in enumerate(items):
    print(i, item)
```

### with文でリソースを安全に扱う
```py
# ❌ 非Pythonic
f = open('file.txt')
data = f.read()
f.close()

# ✅ Pythonic
with open('file.txt') as f:
    data = f.read()
```

### 具体例（ソースコード全体）

```py
def process_user_profile(user):
    # バリデーション（年齢が0以下またはNoneなら終了）
    if user is None or user.get("age", 0) <= 0:
        return "Invalid user data"

    # 年齢によってカテゴリを分類（条件分岐と値の設定）
    category = "adult" if user["age"] >= 18 else "minor"

    # 趣味を大文字に変換（リスト内包表記）
    hobbies = [hobby.upper() for hobby in user.get("hobbies", [])]

    # ユーザー名の並びを入れ替え（変数のスワップ）
    first_name = user.get("first_name", "")
    last_name = user.get("last_name", "")
    first_name, last_name = last_name, first_name  # 入れ替え

    # 位置情報がなければデフォルトを設定（辞書.getの活用）
    location = user.get("location", "Unknown")

    # 好きな色が特定の候補に含まれるかチェック（複数の比較）
    valid_colors = {"red", "blue", "green"}
    favorite_color = user.get("favorite_color", "none")
    color_status = "valid" if favorite_color in valid_colors else "invalid"

    # 出力（enumerateで番号付きで表示）
    print(f"User: {first_name} {last_name}")
    print(f"Age category: {category}")
    print(f"Location: {location}")
    print(f"Favorite color: {favorite_color} ({color_status})")
    print("Hobbies:")
    for i, hobby in enumerate(hobbies, 1):
        print(f"  {i}. {hobby}")

    return "Profile processed successfully"

if __name__ == '__main__':
    
    user_info = {
    "first_name": "Alice",
    "last_name": "Smith",
    "age": 25,
    "hobbies": ["reading", "cycling", "coding"],
    "location": "Tokyo",
    "favorite_color": "blue"
    }

    result = process_user_profile(user_info)
    print(result)
```

```bash
# 出力
User: Smith Alice
Age category: adult
Location: Tokyo
Favorite color: blue (valid)
Hobbies:
  1. READING
  2. CYCLING
  3. CODING
Profile processed successfully
```