
# 🚀 GitHubリポジトリを作成してローカルからPushするまでの手順まとめ


## 📦 ステップ① GitHubでリポジトリを作成する

### ✅ 手順
- GitHubにログイン
- 右上の「＋」 → `New repository`
- 任意の名前を入力（例：`fastapi-practice`）
- **Public or Private** を選択
- README や .gitignore は追加せずに `Create repository`

---

## 🖥 ステップ② ローカルでプロジェクトを作成・初期化

```bash
cd ~/projects/fastapi-practice  # プロジェクトのディレクトリへ
git init
git add .
git commit -m "initial commit"
```

---

## 🌐 ステップ③ リモートリポジトリを登録

```bash
git remote add origin git@github.com:shinya-kg0/fastapi-practice.git
```

> ※ SSHで接続する場合。HTTPSの場合はURLが異なります。

---

## 🚀 ステップ④ 初回Push

```bash
git push -u origin main
```

---

# 🛠 トラブルシューティング集

---

## ❌ pushで「Authentication failed」エラーが出た

- **原因：** GitHubのHTTPS認証ではパスワードは使えない
- **解決：** Personal Access Token（PAT）を使う or SSH接続に切り替える

---

## ❌ 「Repository not found」エラーが出た

- **原因1：** URLが間違っている（スペルミスやアカウント名のミス）
- **原因2：** リポジトリがプライベートで、SSHキーが正しく登録されていない
- **確認方法：**
  - GitHubで `fastapi-practice` リポジトリが自分のアカウントか確認
  - `git remote -v` で登録されたURLを確認

---

## 🔐 SSH接続がうまくいかないときの対処

### ✅ 使用中のSSHキーを確認

```bash
ssh -T git@github.com -v
```

- `Offering public key: ...` の行で、どの鍵を使おうとしているかがわかる

### ✅ `.ssh/config` に設定を追加

```sshconfig
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
```

### ✅ SSHキーを明示的に追加

```bash
ssh-add ~/.ssh/id_ed25519
```

---

## 📌 補足メモ

- GitHubにSSHキーを登録するのは「Settings」→「SSH and GPG keys」
- `ssh -T git@github.com` で `Hi ユーザー名!` と出れば成功

---

## ✅ 結果

```bash
git push origin main
```

で無事Pushできた！

---

sshキーを新しく作成しpushしたい時は、使用中のSSHキーがどうなっているかをチェックするといいかも

