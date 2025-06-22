# 基本

まずは仮想環境を用意

次の2つを`pip install`
- fastapi
- "uvicorn[standard]"

`uvicorn main:app --reload`で実際にサーバーを実行させる

`http://127.0.0.1:8000/openapi.json`これでJSONの情報を確認できる


`def read_items(q: list[str] | None = Query(default=None, min_length=2, max_length=50)):`
ここでqのバリデーションを定義しているが、Listにすると要素が2個以上になり、strにすると2文字以上になる

`http://localhost:8000/items/?q=foo&q=bar`で情報を取得

一般的なバリデーションとメタデータ:

- alias
- title
- description
- deprecated

文字列のためのバリデーション:

- min_length
- max_length
- regex


また、数値のバリデーションを宣言することもできます:

- gt: より大きい（greater than）
- ge: 以上（greater than or equal）
- lt: より小さい（less than）
- le: 以下（less than or equal）

exampleとして、具体例を設定できる
```py
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```