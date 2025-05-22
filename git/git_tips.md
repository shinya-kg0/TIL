# git stash使ってみる
基本的には、あるブランチで作業中だが、他に作業をしないといけなくなった。  
中途半端なのでコミットはしたくないけど、、、

こんなときに`git stash`で作業を退避できる！


## 基本コマンド

### git stash

このコマンドで変更があるファイルを退避できる。  
`-u`オプションをつけるとuntracked fileまで一緒に退避できる


```bash
git stash hogehoge.py

git stash -u bar.py
```

### git stash list

今退避しているファイルのリストを確認できる。

```bash
$ git stash list
stash@{0}: WIP on test: xxxx
stash@{1}: WIP on commit-sample: xxxx
```

### git stash save <コメント>

退避する理由などをコメントとして残すことができる

```bash
git stash save "xxxの変更"
```


### git stash apply, pop, drop, clear 

stashしたファイルをどうするかの操作
- apply：stashしているファイルを戻す。（stashからは消えない）
- pop：stashしているファイルを戻し、stashから削除する。
- drop：stashされているファイルを削除する。
- clear：すべてのstashファイルを削除する。

`stash@{X}`で任意の順番の変更ファイルに適応できる。

```bash
git stash apply stash@{0}

git stash pop
```

### git stash push -- <ファイル名>

特定ファイルをstashできる。

```bash
git stash push -- git/git_tips.md 
```


## Tips

### ブランチを間違えて作業していた、、、

`git stash`を使うことで簡単に変更内容を本来のブランチに移動できる！

たとえば、特定ファイルのみをstashして、ブランチを変更してpopすれば解決できる！

# ミスった時の対処法

[[Git]コミットの取り消し、打ち消し、上書き](https://qiita.com/shuntaro_tamura/items/06281261d893acf049ed)

[【git】マージしたけどやっぱりやめたい時のやり方4種類](https://qiita.com/chihiro/items/5dd671aa6f1c332986a7)

[Git 間違って rebase しちゃったのを元に戻したい](https://chaika.hatenablog.com/entry/2021/01/18/140000)

## コミットの取り消し

```bash
git reset --soft HEAD^
```

コミット自体を取り消す。

- --softオプション：ワークディレクトリの内容はそのままでコミットだけを取り消したい場合に使用。

- --hardオプション：コミット取り消した上でワークディレクトリの内容も書き換えたい場合に使用。

- HEAD^：直前のコミットを意味する。

- HEAD~{n} ：n個前のコミットを意味する。

  - HEAD^やHEAD~{n}の代わりにコミットのハッシュ値を書いても良い。
  - gitのv1.8.5からは、「HEAD」のエイリアスとして「＠」が用意されている。
  - HEAD~とHEAD^と@^は同じ意味。
  - HEAD^^^とHEAD~3とHEAD~~~とHEAD~{3}と@^^^は同じ意味。

```bash
git revert <コミットID>
```

そのコミットを打ち消す内容のコミット。  
修正内容のコミットも残す。

## コミットメッセージの変更

```bash
git commit --amend
```

## マージの取り消し

```bash
git merge --abort
```

## リベースの取り消し

### リベースの途中（コンフリクト時など）
```bash
git rebase --abort
```

### リベース完了時
```bash
$ git reflog
94677f475 (HEAD) HEAD@{0}: rebase (continue) (finish): XXXXX
94677f475 HEAD@{1}: rebase (continue): XXXXXXX
6cd481228 HEAD@{2}: rebase (continue): XXXXXXX
b43e2b915 HEAD@{3}: rebase (start): XXXXXXX
cb0a55a4e HEAD@{4}: checkout: moving from XXXXX // <- rebase 開始前のココ戻りたい
…

$ git reset --hard HEAD@{4}
```

## ワークツリーに対するミス

- 間違って別のファイルを上書きコピー
- ファイルを間違って消した、、、

```bash
git restore .
```

変更を破棄するコマンドなので、大切な修正がないかをよく確かめるのが重要！

