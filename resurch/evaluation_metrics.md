## 1. 物体検出の指標 (Detection)

主に「物体がそこにあるか、形や向きは正しいか」を測ります。

* **mAP (mean Average Precision):**
最も基本的な指標。物体のクラス（車、歩行者など）ごとに、検出の正確さと網羅性を総合したスコアです。
* **True Positive (TP) 系指標:** mAPでは測れない「ズレ」を詳細に分析します。**値が低いほど高精度**です。
* **mATE (mean Attribute Translation Error):** 中心位置のズレ（m）。
* **mASE (mean Attribute Scale Error):** サイズ（幅・丈・高さ）のズレ（1-IOU）。
* **mAOE (mean Attribute Orientation Error):** 向き（角度）のズレ（rad）。
* **mAVE (mean Attribute Velocity Error):** 速度の推定誤差（m/s）。
* **mAAE (mean Attribute Attribute Error):** 属性（駐車中か走行中かなど）の分類ミス。


* **NDS (nuScenes Detection Score):**
上記すべて（mAPと5つのTP指標）を統合した、nuScenes独自の総合スコア。モデルの総合力を一言で表す際によく使われます。

---

## 2. 物体追跡の指標 (Tracking)

「時間の経過とともに、同一人物・同一車両を正しく追い続けられているか」を測ります。

* **AMOTA / AMOTP:** 追跡の標準的な総合指標。AMOTA（Accuracy）は追跡の正確性を、AMOTP（Precision）は位置の正確性を表します。
* **MOTA / MOTP:**
伝統的な追跡指標。MOTAは誤検出やIDスイッチ（入れ替わり）を考慮し、MOTPは位置のズレを測ります。
* **IDS (ID Switches):**
追跡対象のIDが途中で入れ替わってしまった回数。少ないほど優秀です。
* **RECALL:**
全対象のうち、どれだけ見逃さずに検出・追跡できたかの割合。
* **MOTAR:**
MOTAにRecallの概念を組み込み、より厳密に追跡性能を評価する指標です。

---

## 3. 静的環境・オンライン地図の指標 (Map)

道路の構造（レーンや境界）をどれだけ正確に把握できているかを測ります。

* **クラス別要素:**
* **ped_crossing:** 横断歩道の認識。
* **divider:** 車線境界線（白線・黄線など）の認識。
* **boundary:** 道路の端（縁石やガードレール）の認識。


* **mAP_normal:**
地図要素（ライン）の形状をベクトルとして捉え、その一致度を評価するMap用のmAPです。

---

## 4. プランニングと共通評価 (Planning & Common)

最終的な「走り」の質や、計算の基礎となる指標です。

* **L2 (L2 Distance / Displacement Error):**
モデルが予測した走行軌跡と、実際の正解（GT）の軌跡との直線距離誤差。**プランニングの正確さ**を測る最重要指標の一つです。
* **obj_box_cal:**
物体のバウンディングボックス（外接箱）の計算精度や、その重なり具合に関する評価。
* **RECALL (Planning文脈):**
衝突の危険があるシーンなどで、正しく「停止」や「回避」を選択できたかなどの網羅性を指すこともあります。

---

## 指標の関係性まとめ

| カテゴリ | 総合指標 | 精度(誤差)指標 | 頻度・個数指標 |
| --- | --- | --- | --- |
| **物体検出** | **NDS**, mAP | mATE, mASE, mAOE | - |
| **物体追跡** | **AMOTA**, MOTA | AMOTP, MOTP | IDS |
| **地図・構造** | mAP_normal | - | ped_crossing等 |
| **プランニング** | - | **L2** | - |

