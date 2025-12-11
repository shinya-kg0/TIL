# MMDetection3D

3Dオブジェクト検出に特化したオープンソースライブラリ

LiDAR点群、カメラ画像などを用いた3D検出アルゴリズムを提供、開発の支援を行う

Pytorch、MMCV、MMEngine、MMDetection、Spconvなどのライブラリに依存する。


## 基本的な使い方

### 1. 環境構築とインストール

- Pytorchのインストール
- MMCVとMMEngineのインストール
- MMDetection3Dのインストール
  - リポジトリをクローンして、セットアップスクリプトを実行してインストール


### 2. 設定ファイルの理解

モデルのアーキテクチャ、データセット、学習設定などの情報をまとめて管理する。

`configs/`ディレクトリ内にあり`.py`ファイルで記述

**Configファイル内の主要な要素**

要素 | 役割
 -- | -- 
`model` | ネットワーク構造（バックボーン、ヘッドなど）を定義します。
`dataset` | "使用するデータセット（KITTI, NuScenesなど）やデータ処理パイプライン（アノテーションの読み込み、データ拡張）を定義します。"
`train_cfg`/`test_cfg` | 学習時/テスト時の設定（NMSのしきい値など）を定義します。
`schedule` | 最適化手法（Optimizer）、学習率スケジュール（LR Scheduler）、エポック数などを定義します。


→ 既存のConfigファイル（`pointpillars_hv_secfpn_8xb6-160e_kitti-3d-3class.py`など）をコピー・編集して使用すると簡単。


### 3. モデル推論の実行

学習済みモデルを使って推論すると手軽に試せる。

- 学習済み重み（checkpoint）のダウンロード
  - 使用したいConfigファイルに対応する学習済み重みファイル（`.pth`）をダウンロード
  - MMDetection3Dの公式リポジトリのREADMEやモデルZooにリンクあり
- 推論スクリプト実行
  - 提供されている推論スクリプトがある。（`demo/pcd_demo.py`）

```bash
python demo/pcd_demo.py \
    # 使用する設定ファイル
    configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-3class.py \
    # ダウンロードした学習済み重みファイル
    checkpoints/hv_pointpillars_secfpn_256x256_80e_kitti-3d-3class_20220301_150305-b6d37637.pth \
    # 推論したい点群データファイル（.binや.pcdなど）
    demo/data/kitti/000008.bin \
    # 推論結果を保存するディレクトリ（可視化画像などが生成される）
    --out-dir work_dirs/demo \
    --show # 結果を可視化して表示する場合
```

- 結果の確認
  - `--out-dir`で指定したディレクトリに検出結果のファイルが保存される。

## カスタムデータセットでの学習

1. データセットの準備
  - MMDetection3Dがサポートする形式（KITTI, NuScenesなど）に合わせて点群ファイルやアノテーションを配置する。
2. Configファイルの修正
  - `data`セクションのデータセットのパスとクラス数をカスタムデータセットに合わせて変更する
3. 学習スクリプトの実行
  - 提供されている学習スクリプトを実行（`tools/train.py`）

```bash
python tools/train.py \
    # 独自のデータセットに合わせて修正したConfigファイル
    configs/my_custom/my_pointpillars_config.py
```

