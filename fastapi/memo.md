# 基本

まずは仮想環境を用意

次の2つを`pip install`
- fastapi
- "uvicorn[standard]"

`uvicorn main:app --reload`で実際にサーバーを実行させる

`http://127.0.0.1:8000/openapi.json`これでJSONの情報を確認できる

