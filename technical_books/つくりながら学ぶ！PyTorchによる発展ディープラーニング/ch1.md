# 第1章 画像分類と転移学習

※ ソースコード類はすべて[このページ](https://github.com/YutaroOgawa/pytorch_advanced)を参考にしています。

この章ではVGGを使って画像分類をしているが、すべては扱わない。  
勉強になった部分をトピックとしてまとめる。

VGGは画像の特徴量を抽出する`features`モジュールと抽出された特徴量からクラスを予測するための`classifier`モジュールで構成されている。

- `features`モジュール
  - 3x3のカーネルを使って畳み込み、ReLU、Poolingを行う。
  - これらのセットが積み重なっている
- `classifier`モジュール
  - 全結合層、ReLU、Dropoutを使って最終的には1000分類になるように出力のユニット数が調整されている。

## 画像の前処理について

画像をモデルに入力するには、さまざまな前処理が必要である。
- 224x224にリサイズする（VGGの場合）
- 色情報を規格化する
- テンソルに変換する

さらに、学習時にはデータオーギュメンテーションを行うことで学習データを増やす。次のようなメリットがある。  
（既存の学習データを加工・変換することでデータ量を人工的に増やす技術）
- メリット
  - データ不足の解消
  - モデルの汎化性能向上
  - 過学習の防止
- 主な手法
  - 回転、拡大縮小、並行移動、反転、ノイズ付加、色調整



### `Compose`を使った前処理の効率化

`torchvision`の`transformers`を使って前処理を行うが、次のように前処理クラスを定義することができる


<details><summary>前処理クラス</summary>


```python
from torchvision import models, transforms

# 入力画像の前処理のクラス
class BaseTransform():
    """
    画像のサイズをリサイズし、色を標準化する。

    Attributes
    ----------
    resize : int
        リサイズ先の画像の大きさ。
    mean : (R, G, B)
        各色チャネルの平均値。
    std : (R, G, B)
        各色チャネルの標準偏差。
    """

    def __init__(self, resize, mean, std):
        self.base_transform = transforms.Compose([
            transforms.Resize(resize),  # 短い辺の長さがresizeの大きさになる
            transforms.CenterCrop(resize),  # 画像中央をresize × resizeで切り取り
            transforms.ToTensor(),  # Torchテンソルに変換
            transforms.Normalize(mean, std)  # 色情報の標準化
        ])

    def __call__(self, img):
        return self.base_transform(img)
```
</details>

<details><summary>前処理クラス（学習、推論、拡張）</summary>


```python
from torchvision import models, transforms

# 入力画像の前処理をするクラス
# 訓練時と推論時で処理が異なる


class ImageTransform():
    """
    画像の前処理クラス。訓練時、検証時で異なる動作をする。
    画像のサイズをリサイズし、色を標準化する。
    訓練時はRandomResizedCropとRandomHorizontalFlipでデータオーギュメンテーションする。


    Attributes
    ----------
    resize : int
        リサイズ先の画像の大きさ。
    mean : (R, G, B)
        各色チャネルの平均値。
    std : (R, G, B)
        各色チャネルの標準偏差。
    """

    def __init__(self, resize, mean, std):
        self.data_transform = {
            'train': transforms.Compose([
                transforms.RandomResizedCrop(
                    resize, scale=(0.5, 1.0)),  # データオーギュメンテーション
                transforms.RandomHorizontalFlip(),  # データオーギュメンテーション
                transforms.ToTensor(),  # テンソルに変換
                transforms.Normalize(mean, std)  # 標準化
            ]),
            'val': transforms.Compose([
                transforms.Resize(resize),  # リサイズ
                transforms.CenterCrop(resize),  # 画像中央をresize×resizeで切り取り
                transforms.ToTensor(),  # テンソルに変換
                transforms.Normalize(mean, std)  # 標準化
            ])
        }

    def __call__(self, img, phase='train'):
        """
        Parameters
        ----------
        phase : 'train' or 'val'
            前処理のモードを指定。
        """
        return self.data_transform[phase](img)

```

</details>


## VGGの出力層を変更して転移学習を可能にする

### 出力層を変更する
モデルを定義した後に、出力層のインデックスを指定して付け替える操作を行う。（例えば線形変換）

```py
# VGG16の最後の出力層の出力ユニットをアリとハチの2つに付け替える
net.classifier[6] = nn.Linear(in_features=4096, out_features=2)
```

### 層別に勾配計算をするかどうかを設定する
以下の例では、出力層の重みとバイアスだけ学習させるように設定している。

```py
# 転移学習で学習させるパラメータを、変数params_to_updateに格納する
params_to_update = []

# 学習させるパラメータ名
update_param_names = ["classifier.6.weight", "classifier.6.bias"]

# 学習させるパラメータ以外は勾配計算をなくし、変化しないように設定
for name, param in net.named_parameters():
    if name in update_param_names:
        param.requires_grad = True
        params_to_update.append(param)
        print(name)
    else:
        param.requires_grad = False
```