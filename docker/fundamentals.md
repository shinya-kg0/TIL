- Nginxのようなミドルウェア系（Webサーバー、DBなど）  
→ すでに最適化された完成済みイメージが用意されているので、docker run でそのまま使える。
- Pythonアプリのような開発系（コードを書く対象）  
→ 自分のコードやパッケージが必要なので、Dockerfileで定義して自分用のイメージを作る。


RUNはイメージを作成する前に実行されるものなのです。一方、CMDはイメージ作成後に実行されます。

CMDは一回しか実行できない  
CMDを複数実行するには.shファイルを用意する必要がある。


# nginxで一連の流れを体験

1. イメージを取ってくる（pull）
2. コンテナの起動
3. コンテナ内で作業
4. コンテナの削除

## 使ったコマンド

```bash
# イメージを取得
docker pull nginx

# イメージの確認
docker image ls

# 動作中のコンテナを確認[停止中も含む]
docker ps [-a]

# コンテナの起動
docker run --name my-nginx -d -p 8080:80 nginx

# コンテナに入る
docker exec -it my-nginx bash

# コンテナを止める/はじめる
docker stop/start my-nginx

# コンテナを削除（イメージは残る）
docker rm my-nginx

# イメージの削除
docker rmi nginx
```

`docker run` のオプション

- -name my-nginx → コンテナに「my-nginx」という名前をつける
- d → バックグラウンドで起動（画面がロックされない）
- p 8080:80 → ホストPCの8080番とコンテナの80番をつなげる
- nginx → 起動元のイメージ名

**結果**：

ブラウザで [http://localhost:8080](http://localhost:8080/) を開くと、Nginxの初期ページが表示されます。

# 最小のPythonアプリ実行を体験

コンテナを作ったら、コマンドが実行されてprintが表示されるだけの最小構成

## ディレクトリ構成

```
my-python-app/
├── app.py
├── requirements.txt
├── Dockerfile
```

```python
# app.py
print("Hello from Docker Python!")
```

```
# requirements.txt
requests
```

## Dockerfileを作ってみる

```docker
# ベースとなるPythonイメージを指定
FROM python:3.10-slim

# 作業ディレクトリを作成
WORKDIR /app

# ローカルのファイルをコンテナ内にコピー
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# 起動時に実行されるコマンド
CMD ["python", "app.py"]
```

## Dockerイメージをビルドする

```bash
docker build -t my-python-app .
```

- t：イメージに名前をつける
- .：現在のディレクトリにある Dockerfile を使う

無事成功したらイメージが完成している（`docker images`で確認）

## コンテナの実行

```docker
docker run --rm my-python-app
```

そもそもこのコンテナは一時的にPython環境を作って実行しているプロセスなので、実行したらコンテナは削除される

# FastAPIを立ち上げる

## **🚀 STEP 2｜FastAPIをDockerで立ち上げる**

### **🎯 目標**

- FastAPIアプリをDockerで動かす
- http://localhost:8000 でAPIにアクセスできるようにする
- http://localhost:8000/docs にSwagger UIが表示される

---

## **📁 1. プロジェクト構成を準備**

まずは作業フォルダを作成します：

```docker
fastapi-docker-app/
├── app/
│   └── main.py
├── requirements.txt
└── Dockerfile
```

---

## **📝 2. ファイルを作成・編集**

**🔸app/main.py**

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Docker + FastAPI!"}
```

**🔸 requirements.txt**

```python
fastapi
uvicorn[standard]
```

**🔸 Dockerfile**

```docker
# ベースイメージ
FROM python:3.10-slim

# 作業ディレクトリを作成
WORKDIR /app

# 依存ファイルをコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリのコードをコピー
COPY ./app ./app

# ポートを開放
EXPOSE 8000

# 起動コマンド
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

## **⚙️ 3. Dockerイメージをビルド**

```docker
docker build -t fastapi-docker-app .
```

## **🚀 4. コンテナを起動**

```bash
docker run -d \
  --name fastapi-dev \
  -p 8000:8000 \
  -v "$PWD/app":/app/app \
  fastapi-docker-app
```

## 補足：Makefileを使う

```makefile
# イメージ・コンテナ名
IMAGE_NAME=fastapi-docker-app
CONTAINER_NAME=fastapi-container
PORT=8000

# ビルド（イメージ作成）
build:
	docker build -t $(IMAGE_NAME) .

# 起動（バックグラウンド）
up:
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):8000 $(IMAGE_NAME)

# 開発モード（ホットリロード + bind mount）
dev:
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):8000 \
		-v $(PWD)/app:/app/app \
		$(IMAGE_NAME)

# ログ確認
logs:
	docker logs -f $(CONTAINER_NAME)

# シェルに入る
bash:
	docker exec -it $(CONTAINER_NAME) bash

# 停止
stop:
	docker stop $(CONTAINER_NAME)

# 削除（停止してから削除）
rm:
	docker stop $(CONTAINER_NAME) && docker rm $(CONTAINER_NAME)

# 再起動（使い回し）
restart:
	docker restart $(CONTAINER_NAME)

# イメージ・コンテナすべて削除（危険！）
clean:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	docker rmi $(IMAGE_NAME) || true
```

```bash
make build     # Dockerイメージをビルド
make up        # コンテナ起動
make logs      # ログを見る
make bash      # コンテナに入る
make stop      # 停止
make rm        # コンテナ削除
make dev       # 開発用モード（ホットリロード対応）
```

## **📦 Step 1｜PostgreSQLコンテナを単体で立ち上げる**

**📁 プロジェクト直下に.envを作成**

```bash
POSTGRES_DB=example_db
POSTGRES_USER=example_user
POSTGRES_PASSWORD=example_pass
```

**▶ コンテナ起動コマンド（単体実行）**

```bash
docker run -d \
  --name postgres-db \
  -e POSTGRES_DB=test_db \
  -e POSTGRES_USER=test_user \
  -e POSTGRES_PASSWORD=test_pass \
  -p 5432:5432 \
  postgres:15
```

```bash
docker exec -it postgres-db psql -U test_user -d test_db
```

## **🛠 Step 2｜FastAPI側をPostgreSQLと接続できるようにする**

### **🔧 依存ライブラリの追加**

requirements.txt に追記：

```bash
psycopg2-binary
sqlalchemy
```

---

### **📝 FastAPIアプリ側のDB接続コード例（同期版）**

app/db.py などに：

```python
from sqlalchemy import create_engine

DB_URL = "postgresql://test_user:test_pass@localhost:5432/test_db"
engine = create_engine(DB_URL, echo=True)
```

ここではまずローカル接続（localhost:5432）で確認

後ほどcomposeにしたら db:5432 へ変更します

---

## **📋 Step 3｜docker-compose.yml を使って一括管理**

### **🔧docker-compose.yml**

```yaml
version: "3.8"

services:
  web:
    build:
      context: .
    container_name: fastapi-container
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app/app
    depends_on:
      - db
    environment:
      - DB_URL=postgresql://example_user:example_pass@db:5432/example_db

  db:
    image: postgres:15
    container_name: postgres-container
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=example_db
      - POSTGRES_USER=example_user
      - POSTGRES_PASSWORD=example_pass
```

**環境変数やDB URLも.envに切り出す方がいい**

---

## **✅ FastAPI側のコード修正（compose対応）**

```python
import os
from sqlalchemy import create_engine

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL, echo=True)
```

**🚀 起動方法**

```bash
docker-compose up --build
```

---

## **✅ 状況確認**

- FastAPI： http://localhost:8000/
- Swagger UI： http://localhost:8000/docs
- PostgreSQL：コンテナ名 postgres-container で動作中

---

## **📄Makefile（docker-compose 対応版）**

```makefile
# サービス名（compose.yml の service 名）
WEB_SERVICE=web
DB_SERVICE=db

# コンテナ起動（ビルド含む）
up:
	docker-compose up -d --build

# 停止
stop:
	docker-compose stop

# 完全に停止＆削除
down:
	docker-compose down

# ログ表示（全体）
logs:
	docker-compose logs -f

# Webコンテナにbashで入る
bash:
	docker-compose exec $(WEB_SERVICE) bash

# DBコンテナにpsqlで入る
psql:
	docker-compose exec $(DB_SERVICE) psql -U example_user -d example_db

# 再ビルド（キャッシュなし）
rebuild:
	docker-compose build --no-cache

# Webコンテナを再起動
restart:
	docker-compose restart $(WEB_SERVICE)

# イメージや未使用リソースを一掃（注意！）
prune:
	docker system prune -f
```

## **SQLAlchemyによるテーブル定義＋FastAPIでのCRUD API実装**

---

## **🎯 目標（このステップでやること）**

1. SQLAlchemyで簡単なモデル（テーブル）を定義する
2. PostgreSQLにテーブルを作成する
3. FastAPIでCRUD APIを実装し、Swagger UIから操作できるようにする

---

## **🧱 1. プロジェクト構成の追加**

```makefile
fastapi-docker-app/
├── app/
│   ├── main.py          # FastAPIエントリポイント
│   ├── db.py            # DB接続用の共通処理
│   ├── models.py        # テーブル定義（SQLAlchemy）
│   └── crud.py          # データ操作（CREATE/READ）
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
└── Makefile
```

---

## **📝 2. モデル（テーブル）を定義する**

**app/models.py**

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
```

---

## **🔌 3. DB接続とテーブル作成**

**app/db.py**

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

**app/main.py（テーブル作成を追加）**

```python
from fastapi import FastAPI
from app.models import Base
from app.db import engine

app = FastAPI()

# 起動時にテーブルを作成
Base.metadata.create_all(bind=engine)
```

---

## **✍️ 4. CRUD処理を定義する**

**app/crud.py**

```python
from sqlalchemy.orm import Session
from app.models import Item

def create_item(db: Session, name: str, description: str):
    item = Item(name=name, description=description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_items(db: Session):
    return db.query(Item).all()
```

---

## **🌐 5. APIルーティングを追加する**

**app/main.py（更新）**

```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Base
from app.crud import create_item, get_items
from app.db import engine

app = FastAPI()
Base.metadata.create_all(bind=engine)

# DBセッションの依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items")
def create(name: str, description: str, db: Session = Depends(get_db)):
    return create_item(db, name, description)

@app.get("/items")
def read(db: Session = Depends(get_db)):
    return get_items(db)
```

---

## **🚀 6. 実行・確認方法**

```python
make up  # コンテナ起動（ビルド込み）
```

- http://localhost:8000/items → GETでデータ取得
- http://localhost:8000/docs → Swagger UI でPOSTも試せる