参考

- [[入門] Pythonを10倍高速化する実践テクニック集](https://qiita.com/ShigemoriMasato/items/7081c88482e27b7f8535)

# 高速化

## Pythonが遅い理由

1. 動的型付け・・・実行時に型チェック
2. インタープリタ実行・・・コードが逐次解釈
3. GIL（Global Interpreter Lock）・・・並列実行の制限

→ 柔軟性と開発効率の高さとのトレードオフ

## 高速化の基本戦略

- アルゴリズム改善
  - 計算量削減
- C実装ライブラリ活用
  - Numpy/Pandas
- 並列処理
  - asyncio
  - multiprocessing
- JIT/AOTコンパイル
  - Numda
  - Cython

例えば、、、

```py
# 遅い例：純粋なPythonループ
def slow_sum(n):
    total = 0
    for i in range(n):
        total += i
    return total

# 速い例：NumPyのベクトル化
def fast_sum(n):
    return np.arange(n).sum()
```


## 文字列操作の最適化


`+=`で文字列連結は非効率。毎回新しい文字列オブジェクトを作成することになり、O(n^2)の計算量に、、、  

※ 文字列は普遍のオブジェクト

```py
# 遅い例：+=演算子での連結
def build_string_slow(n):
    result = ""
    for i in range(n):
        result += f"item{i},"  # 毎回新しい文字列を作成
    return result[:-1]

# 速い例：joinを使用
def build_string_fast(n):
    parts = []
    for i in range(n):
        parts.append(f"item{i}")
    return ",".join(parts)  # 一度に連結
```


### 文字列操作のベストプラクティス

用途 | 推奨方法 | 理由
 -- | -- | -- 
大量の文字列連結 | str.join() | O(n)の時間計算量
少数の変数埋め込み | f-string | 最速のフォーマット方法
条件付き連結 | リスト + join | 中間リストを活用

- ループ内の文字列連結は`join()`を使う
- 少数なら`f-string`で対応


## リスト操作の高速化（内包表記とNumpy）

通常のforループより内容表記


```py
# 遅い例：通常のforループ
def process_list_slow(data):
    result = []
    for x in data:
        if x > 50:
            result.append(x * 2)
    return result

# 中速例：リスト内包表記
def process_list_medium(data):
    return [x * 2 for x in data if x > 50]

# 速い？例：NumPy
def process_list_fast(data):
    arr = np.array(data)
    mask = arr > 50
    return (arr[mask] * 2).tolist()

```


この比較ではNumpyパターンは遅くなる、、、

- Python → Numpy型の変換オーバーヘッド
- フィルタリング処理は苦手
- 小規模データでは変換コストが支配的

→ 状況によってはリスト内包表記の方がいい場面も、、、（行列計算などは圧倒的にNumpy）

### 使い分けの指針

処理内容は？？

- 条件分岐が多い
  - フィルタリング、簡単な変換
→ リスト内包表記


- 純粋な計算
  - 数値計算、行列計算
→ Numpy



## 非同期処理による高速化

Webスクレイピング、API呼び出し、ファイル読み書きなど、  
I/O待機時間が支配的な処理ではCPUが空いてしまう、、、

```py
# 遅い例：同期的な処理
def fetch_sync(urls):
    results = []
    for url in urls:
        # 実際のHTTPリクエストの代わりに遅延をシミュレート
        time.sleep(0.1)  # I/O待機をシミュレート
        results.append(f"Result from {url}")
    return results

# 速い例：非同期処理
async def fetch_async(urls):
    async def fetch_one(url):
        # 非同期的に待機
        await asyncio.sleep(0.1)
        return f"Result from {url}"
    
    # 全てのタスクを並列実行
    tasks = [fetch_one(url) for url in urls]
    return await asyncio.gather(*tasks)
```


```py
async def fetch_multiple_apis():
    """複数のAPIを並列で呼び出す実践例"""
    urls = [
        'https://api.github.com/users/github',
        'https://api.github.com/users/torvalds',
        'https://api.github.com/users/gvanrossum'
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(fetch_json(session, url))
        
        results = await asyncio.gather(*tasks)
        return results

async def fetch_json(session, url):
    async with session.get(url) as response:
        return await response.json()
```

### 非同期処理の使い分け

タスクの種類 | 推奨手法 | 理由
 -- | -- | -- 
I/Oバウンド | asyncio | 単一スレッドで効率的
CPUバウンド | multiprocessing | 真の並列実行
混在型 | concurrent.futures | 柔軟な選択が可能

I/Oバウンドなタスクは非同期処理で対応。  
`asyncio`を使って単一スレッドでも効率的に処理できる。


## 条件分岐の最適化

冗長なif/elseを回避したい。

- 線形探索・・・最悪全ての条件を評価
- 保守性の低下・・・条件が増えるとコードが肥大化
- テストの困難さ・・・全ての分岐をカバーするのは大変

```py
# 遅い例：多段if-elif文
def process_command_slow(command):
    if command == 'start':
        return 1
    elif command == 'stop':
        return 2
    elif command == 'pause':
        return 3
    elif command == 'resume':
        return 4
    ...
    else:
        return 0

# 速い例：辞書ベース
COMMAND_MAP = {
    'start': 1, 'stop': 2, 'pause': 3, 'resume': 4,
    'restart': 5, 'status': 6, 'config': 7, 'update': 8,
    'delete': 9, 'create': 10, 'list': 11, 'help': 12
}

def process_command_fast(command):
    return COMMAND_MAP.get(command, 0)
```

```py
# 関数を値として持つ辞書パターン
def handle_start():
    return "Starting service..."

def handle_stop():
    return "Stopping service..."

def handle_status():
    return "Service is running"

# ディスパッチャー辞書
HANDLERS = {
    'start': handle_start,
    'stop': handle_stop,
    'status': handle_status,
}

def process_command(command):
    handler = HANDLERS.get(command, lambda: "Unknown command")
    return handler()

```

```py
# Python 3.10以降で使えるmatch文
def process_data(data):
    match data:
        case {'type': 'user', 'name': name}:
            return f"User: {name}"
        case {'type': 'product', 'id': id}:
            return f"Product ID: {id}"
        case _:
            return "Unknown data"

```

## Numpyによるベクトル化

```py
# 速い例：NumPyの行列乗算
def matrix_multiply_fast(A, B):
    return np.dot(A, B).tolist()
```

```py
# 良い例：ベクトル化された操作
arr = np.arange(1000000)
result = np.sqrt(arr) * 2 + 1

# 悪い例：Pythonループの使用
result = np.zeros(1000000)
for i in range(1000000):
    result[i] = np.sqrt(arr[i]) * 2 + 1
```

### 得意・不得意

処理内容 | 性能特性 | 期待される高速化
 -- | -- | -- 
行列演算 | 最適化されたBLAS/LAPACK使用 | 50-600倍
要素ごとの数学関数 | ベクトル化により高効率 | 10-100倍
統計処理 | C実装による高速処理 | 10-50倍
条件フィルタリング | 型変換オーバーヘッドあり | 0.5-2倍
複雑な条件分岐 | Python側処理が支配的 | 性能低下の可能性


## メモリ効率の最適化

大量のデータを扱う時に、メモリ使用量は実行速度に直接影響する。

- メモリ不足・・・スワップ発生（極端な速度低下）
- キャッシュミス・・・メモリアクセスの遅延
- ガベージコレクション・・・一時的な処理停止

例えば、リストを使うと全てメモリ上に展開することになる。

```py
# リスト（全データをメモリに保持）
squares_list = [x**2 for x in range(1000000)]  # 約8MB

# ジェネレータ（必要時に計算）
squares_gen = (x**2 for x in range(1000000))   # 約120バイト
```

```py
# 遅い例：全データをメモリに保持
def process_data_slow(n):
    # 大きなリストを作成
    data = [i**2 for i in range(n)]
    # フィルタリング
    filtered = [x for x in data if x % 2 == 0]
    # 集計
    return sum(filtered)

# 速い例：ジェネレータを使用
def process_data_fast(n):
    # ジェネレータ式でメモリ効率化
    data = (i**2 for i in range(n))
    filtered = (x for x in data if x % 2 == 0)
    return sum(filtered)
```

```py
def read_large_file(file_path):
    """大きなファイルを1行ずつ処理"""
    with open(file_path, 'r') as f:
        for line in f:  # ファイル全体をメモリに読み込まない
            yield line.strip()

def process_csv_data(file_path):
    """CSVファイルを効率的に処理"""
    for line in read_large_file(file_path):
        if line and not line.startswith('#'):
            yield line.split(',')

# 使用例
total = sum(
    float(row[2]) 
    for row in process_csv_data('large_data.csv')
    if len(row) > 2
)
```

### メモリ効率化のテクニック

テクニック | 効果 | 使用場面
 -- | -- | -- 
ジェネレータ | メモリ使用量を劇的に削減 | 大量データの逐次処理
itertools | 無限イテレータも扱える | 組み合わせ・順列生成
NumPy ビュー | コピーを避ける | 配列の部分参照
`__slots__` | クラスのメモリ削減 | 大量のインスタンス生成

ファイル処理やデータストリーミングなどでジェネレータは活躍する。


## JITコンパイラの活用

JIT（Just-In-Time）コンパイラとはPythonコードを実行時に機械語にコンパイルする技術。

```py
# Numba JITコンパイル版
@jit  # この1行を追加するだけ
def monte_carlo_pi_fast(n):
    count = 0
    for i in range(n):
        x = np.random.random()
        y = np.random.random()
        if x*x + y*y <= 1:
            count += 1
    return 4.0 * count / n
```

## プロファイリングと最適化戦略

> 早すぎる最適化は諸悪の根源である

最適化の前に、どこがボトルネックなのかを正確に把握することが重要。  
推測に基づく最適化はNG。

問題の種類によって、対応が変わってくる

- 計算量 → アルゴリズム改善
- 数値計算 → ライブラリ活用
- I/O待機 → 並列化
- ループ処理 → JIT/Cython

時間だけでなく、メモリのプロファイリングも大事。


### 最適化のベストプラクティス

1. 測定なくして最適化なし・・・推測ではなくデータに基づく
2. パレートの法則・・・20%のコードが80%の時間を消費
3. 段階的な最適化・・・一度に全てを変更しない
4. 可読性とのバランス・・・過度な最適化は避ける


### 実装の優先順位

1. アルゴリズムの見直し - 最も効果的
2. 適切なデータ構造の選択（list, set, dict）
3. ライブラリの活用（Numpy, Pandas）
4. 並列化・非同期化（I/Oバウンドな処理）
5. JIT/AOTコンパイル - 最後の手段