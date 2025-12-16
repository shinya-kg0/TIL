# 基本文法

## SERECT FROM

nameとfeature列を取得  
（`*`で全カラム選択、ただ列名は絞った方がパフォーマンス○）

```sql
SERECT name, feature
FROM kimetsu;
```

カラム名を変更

```sql
SERECT name AS '名前', feature AS '特徴'
FROM kimetsu;
```

## DISTINCT

呼吸を重複なしで取得

```sql
SERECT DISTINCT(kokyu)
FROM kimetsu;
```

## WHERE

条件指定

```sql
SELECT name, kawaii
FROM eva
WHERE kawaii > 5;
```

両方を満たす（AND）

```sql
SELECT name, kawaii
FROM eva
WHERE kawaii > 5 AND role = 'パイロット';
```

どちらかを満たす（OR）

```sql
SELECT name, kawaii
FROM eva
WHERE kawaii > 5 OR role = 'パイロット';
```

〜の間に指定（BETWEEN）

```sql
SELECT name, kawaii
FROM eva
WHERE kawaii BETWEEN 4 AND 6;
```

まとめて指定（IN, NOT IN）

```sql
SELECT *
FROM eva
WHERE role IN ('パイロット', '作戦部長')
```

あいまい検索（LIKE）

```sql
SELECT *
FROM eva
WHERE name LIKE 'ア%';
```

値が不明、値が入っている（IS NULL, IS NOT NULL）

```sql
SELECT *
FROM eva
WHERE role IS NULL
```

## LIMIT

上限指定  
→ パフォーマンスを下げないために基本設定しておく！

2行のレコードを取得

```sql
SELECT *
FROM eva
LIMIT 2;
```


## ORDER BY

並び替え

```sql
SELECT *
FROM eva
ORDER BY kawaii;
```

降順（DESC）

```sql
SELECT *
FROM eva
ORDER BY kawaii DESC;
```

- SERECTでつけた別名も指定できる
- SERECTに指定していない列や、集約関数も渡せる


## GROUP BY

同じ項目のデータを集計する（複数のデータごと集計したい）

日ごとの会員登録数を集計

```sql
SELECT created_day, COUNT(name)
FROM members
GROUP BY created_day;
```

日毎の会員登録数をチャンネルごとに集計

```sql
# エラーが出るパターン、、、
# 同じ日に複数のチャネルがあり、どの値を入れるかわからない、、、
SELECT created_day, channel, COUNT(name)
FROM members
GROUP BY created_day;
```

軸になるカラムを全てORDER BYに指定。  
なんの値が入るかをSQLが特定できるようにする。

```sql
# 正しい例
SELECT created_day, channel, COUNT(name)
FROM members
GROUP BY created_day, channel;
```

日毎の会員登録者の平均年齢と最大年齢を出す

```sql
SELECT created_day, AVG(age), MAX(age)
FROM members
GROUP BY created_day;
```

# テーブル結合（INNER JOIN、　OUTER JOIN） 

データ集計漏れが発生する可能性があるので注意！

## INNER JOIN

積集合で結合（条件にマッチするレコードがないものは削除される）

```sql
SELECT m.name, h.planet
FROM martians AS m
INNER JOIN histories AS h ON m.id = h.martians_id;
```

## OUTER JOIN

もし条件にマッチしないレコードも含めたい時は、OUTER JOIN  
条件に合わなければnullが入る

```sql
SELECT m.name, h.planet
FROM martians AS m
LEFT OUTER JOIN histories AS h ON m.id = h.martians_id;
```


# CASE式

条件で処理した後集計したい！  
集計関数や、GROUP BYと相性○


```sql
SELECT 
    CASE WHEN pref_name IN ('京都', '大阪') THEN '関西'
    WHEN pref_name IN ('福岡', '佐賀') THEN '九州'
    ELSE NULL
    END AS distinct,
    SUM(population)
FROM
    populations
GROUP BY 
    CASE WHEN pref_name IN ('京都', '大阪') THEN '関西'
    WHEN pref_name IN ('福岡', '佐賀') THEN '九州'
    ELSE NULL
    END;
```

※ 条件処理した後GROUP BYしたい時はどちらもCASE式を書く！

# サブクエリ

平均以上の価格を出す

```sql
SELECT *
FROM items
WHERE price >= (SELECT AVG(price)
                FROM items);
```

カテゴリーごとに平均価格以上の商品を抽出

```sql
# エラーが出る例
# これだと複数の結果が返ってきて、何と比較すればいいかわからない、、、
# 90000, 50000 → カテゴリーの数分
SELECT *
FROM items
WHERE price >= (SELECT AVG(price)
                FROM items
                GROUP BY category);
```

相関サブクエリを使えば解決できる！  
（実行は重い、、、）

```sql
SELECT *
FROM items AS i1
WEHERE price >= (SELECT AVG(price)
                FROM items AS i2
                WHERE i1.category = i2.category
                GROUP BY category);
```


# 検索の基本

- 条件式内にも計算式を入れられる。

```sql
SELECT shohin_mei, hanbai_tanka, shiire_tanka
FROM Shohin
WHERE hanbai_tanka - shiire_tanka > 500
```

```sql
SELECT shohin_mei, hannbai_tanka,
       hannbai_tanka * 2 AS "hannbai_tanka x2"
FROM Shohin;
```

- NULLを計算すると答えはNULLになる
- ANDはORより強いのでOR優先したい時は`()`で囲む

- NULLを含む真理値は注意が必要
  - 真、偽だけでなく、不明（UNKNOWN）がある

# 集約と並べ替え

- `COUNT()`は引数でNULLの扱いが変わる
  - `COUNT(*)`: 全行の数（NULLも含まれる）
  - `COUNT(column)`: 値が入っている数を集計（NULLは含まれない）

- 集約関数はNULLを無視する
  - 基本的には列を引数に指定するので

- `MAX()`, `MIN()`は大体のデータ型に適応できる
  - 例えば、日付など

- `WHERE()`: 行に対する条件指定
- `HAVING()`: グループに対する条件指定（GROUP BYしたあと）
  - 集約キーに対する条件など、どちらにも書ける場合は`WHERE`を使う
  - テーブルは早く小さくした方がいい

# 複雑な問い合わせ

## サブクエリ

- スカラサブクエリ：戻り値がスカラになる

```sql
SELECT shohin_id,
       shohin_mei,
       hanbai_tanka,
       (SELECT AVG(hanbai_tanka)
          FROM Shohin) AS avg_tanka
```

- 相関サブクエリ
  - 小分けにしたグループ内での比較をするときに使う
  - 集合のカットを行なっている

```sql
SELECT shohin_bunrui, shohin_mei, hanbai_tanka
  FROM Shohin AS S1
 WHERE hanbai_tanka > (SELECT AVG(hanbai_tanka)
                         FROM Shohin AS S2
                        -- 同じ商品分類内で比較を行うことを明示
                        WHERE S1.shohin_bunrui = S2.shohin_bunrui
                        GROUP BY shohin_bunrui);
```


# 関数、述語、CASE式

- `CURRENT_TIMESTAMP`: 現在の日時
- `EXTRACT()`: 日付要素の切り出し

```sql
SELECT CURRENT_TIMESTAMP,
       EXTRACT(YEAR   FROM CURRENT_TIMESTAMP) AS year,
       EXTRACT(MONTH  FROM CURRENT_TIMESTAMP) AS month,
       EXTRACT(DAY    FROM CURRENT_TIMESTAMP) AS day,
       EXTRACT(HOUR   FROM CURRENT_TIMESTAMP) AS hour,
       EXTRACT(MINUTE FROM CURRENT_TIMESTAMP) AS minute,
       EXTRACT(SECOND FROM CURRENT_TIMESTAMP) AS second,

```

- INの引数にサブクエリ

```sql
SELECT shohin_mei, hanbai_tanka
  FROM Shohin
 WHERE shohin_id IN (SELECT shohin_id
                       FROM TenpoShohin
                      WHERE tenpo_id = '000c')
```

- COALESCEの使い方

```sql
SELECT COALESCE(TS.tempo_id, "不明") AS tempo_id,
       COALESCE(TS.tempo_mei, "不明") AS tempo_mei
       S.shohin_id,
       S.shohin_mei,
       S.hanbai_tanka
  FROM TempoShohin TS RIGHT OUTER JOIN Shohin S
    ON TS.shohin_id = S.shohin_id
ORDER BY tempo_id;
```


# SQLの高度な処理

## ウィンドウ関数

- カットと順序づけの両方の機能を持っている。
- PARTITION BYは省略可能（その時はすべてのレコードで順序づけを行う）
- PARTITIONで区切られた部分集合を「ウィンドウ」と呼ぶ
- 原則、SELECT句のみで使える

```sql
SELECT shohin_mei, shohin_bunrui, hanbai_tanka,
       RANK () OVER (PARTITION BY shohin_bunrui
                      ORDER BY hanbai_tanka) AS ranking
  FROM Shohin;
```

ウィンドウ関数には種類がある

- RANK関数
  - ランキングを算出、同順位がある時は後続の順位が飛ぶ
  - 1, 1, 1, 4, ...
- DENSE_RANK関数
  - 同順位があっても、後続の順位が飛ばない
  - 1, 1, 1, 2, ...
- ROW_NUMBER関数
  - 一連の連番を付与する
  - 1, 2, 3, 4, ...

## ウィンドウ関数（集約関数Ver）

- そのレコードより上のものを全て足している → 累積和

```sql
SELECT shohin_id, shohin_mei, hanbai_tanka,
       SUM(hanbai_tanka) OVER (ORDER BY shohin_id) AS cur_sum
  FROM Shohin;
```

- 移動平均を計算
- オプションの集計範囲は「フレーム」と呼ばれる
- `ROWS 2 PRECEDING`はカレントレコードと2つ前までの3つで算出する
- `FOLLOWING`で後ろのレコードも指定可能

```sql
SELECT shohin_id, shohin_mei, hanbai_tanka,
       AVG(hanbai_tanka) OVER (ORDER BY shohin_id
                                ROWS 2 PRECEDING) AS moving_avg
  FROM Shohin; 
```


```sql
SELECT shohin_id, shohin_mei, hanbai_tanka
       AVG(hanbai_tanka) OVER (ORDER BY shohin_id
                                ROWS BETWEEN 1 PRECEDING AND
                                1 FOLLOWING) AS moving_avg
  FROM Shohin; 
```

- ORDER BYが2つ出てくる時があるが違う処理をしている
- ランキングを作ったときに、順位は保証されない → ORDER BY

```sql
SELECT shohin_id, shohin_mei, hanbai_tanka,
       RANK () OVER (ORDER BY hanbai_tanka) AS ranking
  FROM Shohin
 ORDER BY ranking;
```

## GROUPING演算子

- 小計・合計を一緒に求めたい（GROUP BYだけでは求められない）
  - 合計してUNIONでくっつけることはできないでもない、、、 
- 一部のDBMSでサポートしていない場合がある
- `ROLLUP`, `CUBE`, `GROUPING SETS`の3種類



- `ROLLUP`
  - 小計と合計を一緒に求める
  - 集計キーは、全て、指定キーで集計
  - 全ての時の集約キーはNULLになる
  - NULLが出るので注意


```sql
SELECT shohin_bunuri, SUM(hanbai_tanka) AS sum_tanka
  FROM Shohin
 GROUP BY ROLLUP(shohin_bunrui);
```

```sql
SELECT shohin_bunuri, tourokubi, SUM(hanbai_tanka) AS sum_tanka
  FROM Shohin
 GROUP BY ROLLUP(shohin_bunrui, tourokubi);
```

- `GROUPING`演算子を使うと、それが単にNULLなのか、超集合行のために生じたNULL化を判別できる


```sql
SELECT CASE WHEN GROUPING(shohin_bunrui) = 1
            THEN '商品分類 合計'
            ELSE shohin_bunrui END AS shohin_bunrui,
       CASE WHEN GROUPING(torokubi) = 1
            THEN '登録日 合計'
            ELSE CAST(torokubi AS VERCCHAR(16)) END AS torokubi,
       SUM(hanbai_tanka) AS sum_tanka
  FROM Shohin
 GROUP BY ROLLUP(shohin_bunrui, torokubi);
```


- `CUBE`
  - 集約キーで切り分けられたブロックを積み上げた立方体のイメージ
  - 集約キーの組み合わせを全て考える


```sql
SELECT CASE WHEN GROUPING(shohin_bunrui) = 1
            THEN '商品分類 合計'
            ELSE shohin_bunrui END AS shohin_bunrui,
       CASE WHEN GROUPING(torokubi) = 1
            THEN '登録日 合計'
            ELSE CAST(torokubi AS VERCCHAR(16)) END AS torokubi,
       SUM(hanbai_tanka) AS sum_tanka
  FROM Shohin
 GROUP BY CUBE(shohin_bunrui, torokubi);
```

## Tips

- NULLが入っているレコードを上に持っていきたい
  - NULLを一番小さい数、日付にキャストする
  - `NULLS FIRST`を使う



```sql
SELECT torokubi, shohin_mei, hanbai_tanka,
       SUN(haibai_tanka) OVER (ORDER BY COREACE(torokubi, CAST('0001-01-01' AS DATE))) AS cur_sum_tanka
       FROM Shohin;
```

```sql
SELECT torokubi, shohin_mei, hanbai_tanka,
       SUN(haibai_tanka) OVER (ORDER BY torokubi NULLS FIRST) AS cur_sum_tanka
       FROM Shohin;
```