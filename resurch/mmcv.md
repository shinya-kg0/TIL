https://mmcv.readthedocs.io/en/master/get_started/introduction.html

# MMCVライブラリまとめ

CVアルゴリズム開発に必要な共通機能を提供する基盤

提供されているモジュールの活用

- 設定ファイルの管理
- 分散学習のユーティリティ
- 様々なオペレーター
- データ処理のパイプライン

## 設定ファイルの管理（Config）

YAML形式の設定ファイルを柔軟に扱う`mmcv.Config`を提供。  
モデルの構造、学習バラメータ、データセットのパスなどを一元管理するのに役立つ。

```py
from mmcv import Config

# 設定ファイルを読み込む
# config/model_a.py のようなファイル名で設定を定義していると仮定
cfg = Config.fromfile('config/model_a.py')

# 設定内容にアクセス
print(cfg.model.type) # 例: 'ResNet50'
print(cfg.optimizer.lr) # 例: 0.01

# 設定内容を上書き
cfg.optimizer.lr = 0.005

# 新しい設定を保存
cfg.dump('new_config.py')
```

## データ変換（Transform）とパイプライン

画像の前処理（リサイズ、クロップ、正規化など）を行うための豊富なデータ変換クラスを提供。  
これらを組み合わせてデータパイプラインを構築できる。

→ MMDetectionなどで非常に重要になる。

```py
from mmcv.transforms import Compose

# データパイプラインの定義例
train_pipeline = Compose([
    dict(type='LoadImageFromFile'), # 画像をファイルから読み込む
    dict(type='RandomFlip', flip_prob=0.5), # ランダムに反転
    dict(type='Resize', scale=(1333, 800), keep_ratio=True), # リサイズ
    dict(type='Normalize', mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True), # 正規化
    dict(type='Pad', size_divisor=32), # 32の倍数になるようにパディング
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels']) # 必要なキーを収集
])

# 実際のデータに適用
# result = train_pipeline(data)
```


## Pytorchオペレーターとユーティリティ

Pytorchには実装されていない、効率的なカスタムオペレーターを提供している。（CUDA/C++で実装）  
（直接インポートして利用可能）

- NMS (Non-Maximum Supperession): 物体検出のバウンディングボックスを整理するために使われる。
- Rol Align: 特徴マップから感心領域を正確に抽出するために使われる。

```py
# from mmcv.ops import nms
# boxes = torch.randn(10, 5) # 10個のバウンディングボックス (x1, y1, x2, y2, score)
# keep, _ = nms(boxes, 0.5) # NMSを実行し、残すインデックスを取得
```


## 分散学習ユーティリティ

複数のGPUや複数のノードを使った学習を用意にするためのユーティリティを提供。

- `MMDistributedDataParallel`: PyTorchのDDP（Distributed Data Parallel）を拡張したもの。
  - DDPとは、データ並列で分散学習をする手法。
  - `model = DistributedDataParallel(model, device_ids=[rank])` のようにラップして、以降は通常どおりforward・backward・optimizer.step()を回すだけで分散学習が行われる。
- get_dist_info, master_only などのヘルパー関数。
  - get_dist_info()
    - 分散かどうかを意識せず、rank / world_size を取得したいとき。
    - 例: sampler の設定、ログの prefix に rank を入れる、など。

  - master_only
    - 以下のように「1 回だけやればいい」処理に付ける： 
      - 標準出力へのログ
      - TensorBoard / WandB ログ
      - モデルや結果画像の保存
      - 評価指標の集約結果の表示

  - get_rank() / get_world_size() / is_master()
    - より細かく rank ごとの処理を分けたいときに使用（例えば rank ごとに異なるシードやデバイス設定を行うなど）。


