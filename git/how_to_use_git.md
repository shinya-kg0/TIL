# 基本のフロー
- 前提
  - リモートリポジトリ（origin）
    - develop, feature/add_form
  - ローカルリポジトリ
    - develop, feature/fix_login
    - remotes/origin/develop, remotes/origin/feature/add_form
  - `feature/add_form`はAさんが開発中
  - `feature/fix_login`は自分が開発しているブランチでまだpushしていない

## リモートブランチが更新されたので取り込みたい、、、
リモート側のdevelopが更新されたので、自分のdevelopにも取り込みたい。今はdevelopブランチにいるとする

- `git fetch origin` をして、ローカルにあるリモート追跡ブランチ`remotes/origin/develop`更新する。
- リモートにあるブランチは全て更新されるので`remotes/origin/feature/add_form`も更新されている.
  - 注意⚠️；fetchはリモートの内容が自分のところで更新されるだけなのでどのブランチにいても大丈夫！
- ここでコンフリクトが起きないように差分を確認`git diff origin/develop`
- 問題なければ、マージする`git merge origin/develop`
  - mergeは今いるブランチに引数に指定しているブランチをマージするので、作業ブランチにいて、  
根元ブランチをマージしないように気をつけて、、、

次は自分の作業ブランチ`feature/fix_login`に変更を取り込む

- すでにfetchをしているので追跡ブランチには取り込んである。
- ここでmergeかrebaseの選択肢が出てくる。（履歴を綺麗にしたいならrebase）
- 差分が問題なければ`git rebase origin/develop`
  - rebeseする時は、作業内容をコミットするかstashで退避させておく


コマンドをまとめてみると次

```bash
git checkout develop

git fetch origin

git diff origin/develop

git merge origin/develop

git checkout feature/fix_login

git rebase origin/develop
```