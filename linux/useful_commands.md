# 使う可能性があるコマンド
zshを前提にしているが、下にlinux用のコマンドを追加している。

- `ls -l | cat -n | less`

ディレクトリ内のファイルを番号を振って確認したい。

パイプラインを使って出力。`-n`は行数を表示させる。

- `du -h /bin/* | sort -n | tail -r | head -n 5`

`du`：ファイルサイズを調べる。`-h`は単位を決めてファイルサイズを表示するオプション  
`tac`：逆順にする  
`tail`：末尾を出力 `-r`で逆順

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


