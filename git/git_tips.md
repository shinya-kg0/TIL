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
