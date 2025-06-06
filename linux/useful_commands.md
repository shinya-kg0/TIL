# 使う可能性があるコマンド
zshを前提にしているが、下にlinux用のコマンドを追加している。

- `ls -l | cat -n | less`

ディレクトリ内のファイルを番号を振って確認したい。

パイプラインを使って出力。`-n`は行数を表示させる。

- `du -h /bin/* | sort -n | tail -r | head -n 5`

`du`：ファイルサイズを調べる。`-h`は単位を決めてファイルサイズを表示するオプション  
`tac`：逆順にする  
`tail`：末尾を出力 `-r`で逆順

```bash
basename /Users/kogashinya/01_work_space/apps/word-counter/backend/main.py
# 出力：main.py
```

- `echo $PATH | sed "s/:/\n/g"`   
  → パス設定をみやすく

- `for i in $(find test -name "hogehoge*.py"); do echo $i; done`  
  → testディレクトリ内のhogehoge関連ファイルに対してループ処理

- `for i in $(ls test_hogehoge*.md); do pandoc -f xx -o xx.docx $i; done`   
  → 指定のディレクトリ内のファイルをdocx化

## `find`コマンド

```bash
# ファイル検索
find . -type f -name '*.txt'

# ディレクトリの検索
find . -type d -name '^2025*.md'

# xargsの応用
find . -type f -name '*.txt' | xargs ls -l
```

- `xargs`を使って、標準入力として引数のリストを与える。
  - サブディレクトリ内のファイルまで含めて全てのファイルに対して任意のコマンドを実行できる

## `wc`コマンド
ファイルのバイト数、単語数、行数を数える（標準入力でもOK）

```bash
# 行数
wc -l /etc/passwd
# 単語数
wc -w /etc/passwd
# バイト数
wc -c /etc/passwd
```

```bash
# ディレクトリ内のファイル・ディレクトリ数を数える
ls -l | wc -l
```

## `sort`コマンド
行を並べ替える

```bash
ps x | sort -k 5

ls -l /bin* | sort -rn -k 5 | head -n 5
```

`-k`：フィールド番号（調べたいカラム）を指定できる  
`-n`：数値で認識して、数値順にソート  
`-r`：逆順にソート

## `uniq`コマンド
重複行を取り除く  
基本的には**ソートしてから**実行

```bash
sort hogehoge.txt | uniq -c | sort -rn
```

`-c`：重複行を数える

## `cut`コマンド
入力の一部を切り出す  
特定の部分だけ取り出すときに便利

```bash
cut -d : -f 1,6,7 /etc/passwd
```

`-d`：区切り文字を指定する。  
`-f`：フィールドを指定（複数指定OK）

## `tr`コマンド
文字の変換、削除する

```bash
# :を,に変換する
cat /etc/passwd | tr : ,

# 複数文字の置換
cat /etc/passwd | tr abc ABC

# 小文字から大文字へ置換
cat /etc/passwd | tr a-z A-Z

# ファイルを指定するとエラー
tr : , /etc/passwd

# 文字の削除（改行の削除）
cat /etc/passwd | tr -d '\n'
```

- 一文字ずつ置換していくので注意！（まとまりでの置換はしない）
- trコマンドは純粋なフィルタなので、ファイルから直接読み込むことはできない
  - ファイルをcatして渡すかリダイレクトで渡す

## `tail`コマンド
末尾部分を表示する

```bash
tail -n 1 /etc/passwd

# リアルタイムで追記を監視する
tail -f output.log
```

`-f`：ファイルへの追記を監視する。  
→ Linuxの運用作業などでログファイルの監視によく使われる

## `diff`コマンド
差分の表示

```bash
diff file1 file2
```

## `grep`コマンド
文字列の検索

```bash
# bashを含む行を出力
grep bash /etc/passwd

# 行番号付きでマッチ結果を表示
grep -n PS1 /etc/passwd

# bashを含まない行を出力
grep -v bash /etc/passwd

# /etcディレクトリ配下の、cshを含むファイル、ディレクトリを検索
ls /etc | grep csh
```

`-n`：行番号付きで出力する  
`-i`：大文字小文字の区別をせずに取得  
`-v`：文字列を含まない行を出力

### 正規表現

条件に合致する文字列集合を表現するための記法（クォートで囲む）

```bash
ls /etc | grep "^sh*" 

ls /etc | grep 'rc$'

grep 't.st' hogehoge.txt

grep '\.org' hogehoge.txt

grep 't[ef]st' hogehoge.txt

grep 'mail[1-4]' hogehoge.txt

# ファイルから空行だけ取り除いて表示する
grep -v '^$' hogehoge.txt

grep '^B[ea]*r$' hogehoge.txt
```

- `^$`：空行を意味する。
- `.*`：任意の文字が0回以上繰り返される。（あらゆる文字列にマッチ）
  - 例）`^ex.*txt$`：exで始まってtxtで終わる行

|メタ文字|意味|
|---|---|
|`^xx`|先頭がxxである|
|`xx$`|xxで終わる|
|`.`|任意の一文字|
|`[ ]`|[ ]の中に含まれる、いずれかの一文字|
|`[^ ]`|[ ]の中に含まれない、いずれかの一文字|
|`\`|直後のメタ文字の意味を打ち消す|


### 拡張正規表現
使えるメタ文字を増やした拡張正規表現というものがある。  
書き方が異なるので注意！

`-E`をつけるか`\`をつければ利用可能

```bash
# 基本正規表現はマッチしない
grep 'Be+r' drink.txt

# これならOK
grep 'Be\+r' drink.txt

# 拡張正規表現ではマッチする
grep -E 'Be+r' drink.txt

grep -E 'Be{1,2}r' drink.txt
grep -E 'Be{2}r' drink.txt
grep -E 'Be{3,}r' drink.txt

grep -E '(Wine){2,}' drink.txt
grep -E 'My (Vodka|Wine)' drink.txt
```

例えば、`[0-9]{3}-[0-9]{4}`という正規表現で郵便番号にマッチする。

|基本正規表現|拡張正規表現|意味|
|---|---|---|
|`*`|`*`|0回以上の繰り返し|
|なし|`+`|1回以上の繰り返し|
|なし|`?`|0または1回の繰り返し|
|`\{m,n\}`|`{m,n}`|m回以上n回以下の繰り返し|
|`\{m\}`|`{m}`|ちょうどm回の繰り返し|
|`\{m,\}`|`{m,}`|m回以上の繰り返し|
|`\(\)`|()|グループ化する|
|なし|`\|`|複数の正規表現をOR条件で連結する|



## `sed`コマンド
非対話型エディタで、編集をその都度していくのではなく、  
編集コマンドを渡して、編集結果を標準出力へ出力する。

**決まったパターンの編集をするときは便利！**  
**元のファイルは変更しない**ので気軽に試せる！

### 行の削除
コマンドは`d`を指定

sedコマンドはアドレスで指定された行のみ作用する  
アドレスを指定しなければ、全ての行に作用する  

アドレスは正規表現でもOK
```bash
# 1行目を削除
sed 1d drink.txt


# 2~5行目を削除
sed 2,5d drink.txt

# 3から最後まで削除
sed '3,$' drink.txt

# Bで始まる行を削除
sed /^B/d drink.txt
```

### 行の表示（あんまり使わない）
コマンドは`p`を指定

そのままだとパターンスペースの内容も出力するので注意

```bash
sed -n 1p drink2.txt
```

### 行を置換する
コマンドは`'s/置換前/置換後/フラグ'`を指定

- アドレスの指定もできる
- 置換は最初の文字列だけが対象。（一行に複数あるときは`g`フラグが必要）
- 正規表現もOK！（常にシングル）
- 空文字を指定して削除もできる
- `-n`, `p`を組み合わせて置換が発生した行だけを表示もできる
- 後方参照：マッチした文字列を置換後に埋め込める

`-n`：パターンスペースを出力しない  
`p`：置換が発生したときの出力する（フラグ）

```bash
# Beer -> Whisky
sed 's/Beer/Whisky/' drink.txt

# 行内の全てをBeer -> Whisky
sed 's/Beer/Whisky/g' drink.txt

# 正規表現もOK
sed 's/B.*r/Whisky/g' drink.txt

# !を削除(空文字を指定)
sed 's/!//g' drink.txt

# 置換が発生した時の行を表示
sed -n 's/!//gp' drink.txt

# 拡張正規表現も使える
sed -E 's/Be+r/Whisky/' drink.txt

# グループ化して置換
# My <文字列>を--<文字列>--に置換
sed 's/My \(.*\)/--\1--/' drink.txt

# アドレスの指定もできる
sed '1,3s/Beer/Whisky/g' drink.txt
```

|基本正規表現|拡張正規表現|
|---|---|
|`\( \)`でグループ化して、`\1`で参照|`( )`でグループ化して、`\1`で参照|

※ 複数のグループ化をしたときは、`\1`, `\2`で順番に参照できる。


## `awk`コマンド
テキストの検索や抽出・加工などの編集操作を行う。

コマンドは`awk <パターン> {アクション}`

- `$2`：2列目、`$0`：すべてのフィールド
- 複数行を表示したいときは`,`をつけておくと見やすい
- `$NF`：最後の列を指定（`list[-1]`のように）`$(NF-1)`もOK
- 正規表現を使って、パターンの指定ができる。（`/`で囲って記述する）
  - 例えば、`/^l/`を指定してシンボリックリンクだけを表示することもできる。
- 他にも条件式などを含めて柔軟に使える。

`-F,`：区切り文字の指定ができる。（←はカンマ区切りの認識）CSVファイルの処理で使える！

```bash
# lsコマンドから5,9列目を表示
ls -l /usr/bin | awk '{print $5,$9}'

# 最後と最後から2番目のフィールドを表示
ls -l /usr/bin | awk '{print $(NF-1),$NF}'

# ファイル名がcpで始まる行のみを対象とする（”~”を忘れない！）
ls -l /usr/bin | awk '$9 ~ /^cp/ {print $5,$9}'

# 行の先頭がlで始まる行のみを対象にする
ls -l /usr/bin | awk '/^l/ {print $5,$9}'

# パスが通っている場所を見やすく表示（grepで追加できる）
echo $PATH | sed 's/:/\n/g'

# 2列目が30の行を表示
awk '$2 == 30' file.txt

# 3列目が100以上の行だけ合計
awk '$3 >= 100 {sum += $3} END {print sum}' file.txt

# 2列目が30以上かつ3列目が「Developer」の行
awk '$2 >= 30 && $3 == "Developer"' file.txt

# プレフィックスを削除して表示
find ~/test -type f -name '*.md' | awk -F/ '{print $NF}'
```

### CSVファイルからスコア集計

出席番号、名前、点数が記録されたCSVファイルの点数の平均値を計算する。

```bash
awk -F, '{print $1,$2,$3}' score.csv

# 点数を取り出す
# $NFを使うことで拡張性を確保
awk -F, '{print $NF}'

# 点数の総和を表示
awk -F, '{sun += $NF} END{print sum}' score.csv

# 平均値を出す
awk -F, '{sum += $NF} END{print "Average:",sum/NR}' score.csv

# .awkファイルから読み出す
cat average.awk
# {sum += $NF} END{print "Average:",sum/NR}
awk -F, -f average.awk score.scv
```

- awkで使われる変数は、宣言や初期化しなくても使える！
  - 数値として扱えば、変数の初期値は0
- ENDブロック内のアクションはすべての入力ファイルを処理し終えてから最後に実行される。
- NR：これまで読み込んだ入力レコード数が代入されている組み込み変数
- `.awk`ファイルで保存しておいて`-f`オプションで呼び出せる。

