# match文

  - Python3.10以降で使える
  - 辞書型でデータを受け取る時には、キーが対応しているかをチェックしている
  - command_data["x"]のようにアクセスするのではなく、case以降に設定した新しい変数を使ってデータを呼び出している

機能 | 目的 | 例
-- | -- | -- 
値のマッチング | 単純な値の比較 | `case 404:`
構造のマッチング | データ構造の形をチェック | `case [_, *rest]:`
変数束縛 | マッチした値を新しい変数に格納 | `case {"action": cmd_name}:`
ifガード | パターン成功後の追加条件チェック | `if duration >= 100:`

活用ケース | 目的 | 活用するパターン
 -- | -- | --
コマンド/メッセージのディスパッチ  | APIやキューから受け取ったJSON/辞書データの「種類」や「形」に応じて、処理関数を振り分ける。 | 構造のマッチング (Dict)
状態遷移/有限オートマトン  | アプリケーションの現在の状態（ステータス）に基づいて次のアクションを決定する。 | 基本的な値のマッチング
ポリモーフィックなオブジェクト処理  | 異なるクラスのオブジェクトが混在するリストを安全かつ効率的に処理する。 | クラス/オブジェクトのマッチング
シーケンスのパターン分解  | 座標や固定長のタプルなど、要素数と並び順が決まっているデータを簡潔に抽出する。 | シーケンスのマッチング (List/Tuple)


```py
# 入力となる値
status_code = 404

match status_code:
    case 200:
        print("OK - 処理成功")
    case 404:
        print("Not Found - ページが見つかりません")
    case 500:
        print("Internal Server Error - サーバー内部エラー")
    case _: # ワイルドカード
        print("その他のステータスコード")
```

```py
# クライアントから受け取ったコマンドデータ
command_data = {"action": "move", "x": 50, "y": 10}

match command_data:
    # パターン1: 移動コマンド (action, x, y のキーが必要)
    case {"action": "move", "x": x_val, "y": y_val}:
        print(f"移動コマンド: X={x_val}, Y={y_val}へ移動")
    
    # パターン2: 攻撃コマンド (action, target のキーが必要)
    case {"action": "attack", "target": target_name}:
        print(f"{target_name}を攻撃")
        
    # パターン3: 終了コマンド (actionキーのみ)
    case {"action": "exit"}:
        print("システムを終")
        
    # どのパターンにもマッチしなかった場合
    case _:
        print("不明なコマンドまたは形式エラー")
```

```py
# 制限時間が200秒なので、条件を満たす
command_A = ["start_game", "level_1", 200]
# 制限時間が50秒なので、条件を満たさない
command_B = ["start_game", "level_1", 50]

for cmd in [command_A, command_B]:
    match cmd:
        # durationをキャプチャした後、if duration >= 100 の条件をチェック
        case [action, level, duration] if duration >= 100:
            print(f"{level}を開始します (制限時間: {duration}秒)。")
        
        case [action, level, duration]:
            # ifガードに失敗したコマンドもこのcaseにはマッチする
            print(f"{level}の制限時間({duration}秒)が短すぎます。")
        
        case _:
            print("不明なコマンドです。")
```

```py
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

def check_point_location(shape):
    match shape:
        # パターン1: x属性が0であるPointインスタンス
        # y属性の値は y_val にキャプチャ
        case Point(x=0, y=y_val):
            print(f"1. 縦軸上の点です (x=0)。Y座標: {y_val}")
            
        # パターン2: y属性が0であるPointインスタンス
        # x属性の値は x_val にキャプチャ
        case Point(x=x_val, y=0):
            print(f"2. 横軸上の点です (y=0)。X座標: {x_val}")
            
        # パターン3: その他のPointインスタンス
        case Point(x=x_val, y=y_val):
            print(f"3. 平面上の点です。座標: ({x_val}, {y_val})")
            
        case _:
            print("4. Pointオブジェクトではありません。")
```

