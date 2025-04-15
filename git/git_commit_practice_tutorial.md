
# 📘 Git コミット整理チュートリアル

## 🎯 目的

Git でマージリクエスト前にコミット履歴を整理するために、実務でよく使われる操作をブランチ上で安全に練習します。

---

## 🧰 前提：練習環境の準備

```bash
mkdir git-commit-practice
cd git-commit-practice
git init

echo "# Git Commit Practice" > README.md
git add README.md
git commit -m "Initial commit"
git checkout -b commit-practice
```

この `commit-practice` ブランチ上で、以下の各ステップを進めていきます。

---

## 🥇 STEP 1：コミットをまとめる（squash）

### ✅ 想定シナリオ：
細かくコミットしすぎたので、マージ前に1つの機能としてまとめたい。

### 🛠 手順：

```bash
echo "Step 1" > feature.txt
git add feature.txt
git commit -m "wip: first step"

echo "Step 2" >> feature.txt
git add feature.txt
git commit -m "wip: second step"

echo "Step 3" >> feature.txt
git add feature.txt
git commit -m "wip: third step"
```

```bash
git rebase -i HEAD~3
```

- 最初の行を `pick`
- 残り2つを `squash`
- メッセージを `feat: implement full feature` に修正

---

## 🥈 STEP 2：コミットを分割する（split）

### ✅ 想定シナリオ：
1つのコミットで複数の変更をしてしまったため、処理ごとに分けたい。

### 🛠 手順：

```bash
echo "Part A" > complex.txt
echo "Part B" >> complex.txt
git add complex.txt
git commit -m "feat: add both A and B"
```

### 🔧 方法①：`git reset` + `git add -p`

```bash
git reset HEAD~1
git add -p
# Aだけステージし、コミット
git commit -m "feat: add part A"
# 残りをステージし、コミット
git add .
git commit -m "feat: add part B"
```

---

## 🥉 STEP 3：コミットメッセージを修正する（reword）

### ✅ 想定シナリオ：
マージ前に誤字を修正したり、メッセージを整えたい。

### 🛠 手順：

```bash
echo "some change" > typo.txt
git add typo.txt
git commit -m "fiex: type"
```

```bash
git rebase -i HEAD~1
# reword を選び、"fix: typo" に変更
```

---

## 🧹 STEP 4：不要なコミットを削除・順序を入れ替える

### ✅ 想定シナリオ：
- 使わない一時的なコミットを削除したい  
- 順番を整理したい

### 🛠 手順：

```bash
echo "delete me" > temp.txt
git add temp.txt
git commit -m "chore: temporary change"

echo "important change" > final.txt
git add final.txt
git commit -m "feat: important feature"
```

```bash
git rebase -i HEAD~2
# chore コミットを drop
# 順番も並び替えて調整
```

---

## 🚨 失敗したときの対処法（安全ネット）

### 🛟 1. `git reflog`：過去の状態に戻れる履歴ログ

```bash
git reflog
# 例）HEAD@{2} などを確認
git reset --hard HEAD@{2}
```

### 🛟 2. `git reset`：やり直しの基本

- ソフトリセット（コミットだけ消す）：
```bash
git reset --soft HEAD~1
```

- ハードリセット（ファイル状態も戻す）：
```bash
git reset --hard HEAD~1
```

### 🛟 3. `git stash`：一時退避

```bash
git stash
# 必要なときに戻す
git stash pop
```

---

## 🧪 ブランチを切って練習を分ける

```bash
git checkout -b squash-practice     # squashだけ練習用
git checkout -b split-practice      # splitだけ練習用
```

---

## 📝 練習用テンプレート（メモとして活用可）

```markdown
# Git Commit 整理 練習メモ

## squash の練習
- before: 3 commits
- after: 1 commit with message "feat: implement full feature"

## split の練習
- before: 1 commit with A+B
- after: 2 commits (A / B)

## reword の練習
- before: fiex: type
- after: fix: typo

## drop / reorder の練習
- drop: chore commit
- reorder: feat -> fix の順に変更
```

---

## ✅ まとめ

| 操作      | 実務頻度 | コマンド例                  |
|-----------|----------|-----------------------------|
| squash    | 高       | `git rebase -i` + `squash`  |
| split     | 中〜高   | `reset` + `add -p`          |
| reword    | 高       | `git rebase -i` + `reword`  |
| drop      | 中       | `git rebase -i` + `drop`    |
| reorder   | 中       | `git rebase -i` 並び替え     |
| restore   | 高       | `git reflog` / `reset`      |
