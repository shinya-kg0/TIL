# 第2章 物体検出
- どんなタスク？
  - 一つの画像の中に含まれている複数の物体に関して、その領域と物体名を特定する。
  - 物体が**どこ**にあって、それは**何**か、またその**確信度**（確率）を出力する。

- インプットとアウトプット
  - 画像をインプットとする
  - アウトプットは次の3種類ある。
    1. 画像のどこに物体が存在するかを示す、バウンディングボックスの位置と大きさの情報
    2. 各バウンディングボックスが何の物体であるのかを示すラベル情報
    3. その検出に対する信頼度(=confidence)


## 物体検出の流れ
1. 画像をリサイズする
2. 様々な大きさとアスペクト比のデフォルトボックスを用意する（ランダム）
3. モデルがそれぞれのDBoxに対してBBoxに修正するオフセット情報4つとDBoxが各クラスの物体である信頼度（クラス数）の合計`n_DBox x (4+n_classes)` 個の情報を計算する
4. 信頼度の高いDBoxを取り出す
5. オフセット情報を使ってBBoxに変形する。ここで重なりが大きいものは最も信頼度が高いBoxだけ残す
6. 最終的なBBoxとそのラベルを出力する。閾値を決めることで検出の調整ができる

### デフォルトボックスからバウンディングボックスへ
デフォルトボックスはボックスのx方向の中心`cx_d`,y方向の中心`cy_d`,高さ`h_d`,幅`w_d`の4つの情報で表現している。

物体検出のモデルは直接バウンディングボックスの情報を出力するのではなく、どのようなオフセット情報があればバウンディングボックスになるかを出力する。  
オフセット情報とは、`∆cx`,`∆cy`,`∆w`,`∆h`のように表され、次の式でバウンディングボックスが表現される。

```math
\displaylines{
cx = cx\_d(1+0.1∆cx) \
cy = cy\_d(1+0.1∆cy) \
w = w\_d * exp(0.2∆w) \
h = h\_d * exp(0.2∆h)
}
```

