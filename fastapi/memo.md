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

普通のデータ型だけでなく、他のデータ型も指定できる

```py
@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: datetime = Body(),
    end_datetime: datetime = Body(),
    process_after: timedelta = Body(),
    repeat_at: Union[time, None] = Body(default=None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }
```

Header(), Cookie()はインポートして使う
※ `convert_underscores=False`でアンダースコアをどうするかも定義できる

header, cookieは`model_config = {"extra": "forbid"}`で余計なものを無視できる

- レスポンスモデル
出力用のレスポンスモデルも定義しておく！


```py
# これはアンチパターン
# パスワードがダダ漏れ
@app.post("/user/")
async def create_user(user: UserIn) -> UserIn:
    return user

# これだとレスポンスとしてパスワードが漏れることはない
@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user
```

デフォルト値が多い時は、変更点以外は省略した方がいいことがある  
→ `response_model_exclude_unset=True`にすれば良い  
→ 逆にincludeにすることで、含めることもできる


- 入力モデル にはパスワードが必要です。
- 出力モデルはパスワードをもつべきではありません。
- データベースモデルはおそらくハッシュ化されたパスワードが必要になるでしょう。

インスタンス化するときに、`**obj.dict()`を使うと便利！

Baseモデルを定義して重複モデルを削減できる！

- レスポンスモデルの定義いろいろ

```py
@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]

@app.get("/items/", response_model=List[Item])
async def read_items():
    return items

@app.get("/keyword-weights/", response_model=Dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}

```

# HTTPステータスコード
- 100以上は「情報」のためのものです。。直接使うことはほとんどありません。これらのステータスコードを持つレスポンスはボディを持つことができません。

- 200 以上は「成功」のレスポンスのためのものです。これらは最も利用するであろうものです。
200はデフォルトのステータスコードで、すべてが「OK」であったことを意味します。
別の例としては、201（Created）があります。これはデータベースに新しいレコードを作成した後によく使用されます。
特殊なケースとして、204（No Content）があります。このレスポンスはクライアントに返すコンテンツがない場合に使用されます。そしてこのレスポンスはボディを持つことはできません。

- 300 以上は「リダイレクト」のためのものです。これらのステータスコードを持つレスポンスは304（Not Modified）を除き、ボディを持つことも持たないこともできます。

- 400 以上は「クライアントエラー」のレスポンスのためのものです。これらは、おそらく最も多用するであろう２番目のタイプです。
例えば、404は「Not Found」レスポンスです。
クライアントからの一般的なエラーについては、400を使用することができます。

- 500以上はサーバーエラーのためのものです。これらを直接使うことはほとんどありません。アプリケーションコードやサーバーのどこかで何か問題が発生した場合、これらのステータスコードのいずれかが自動的に返されます。


```py
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
```

# フォームデータ
フォームデータの入力パラメータを宣言するには、Formを使用する。

例えば、OAuth2仕様が使用できる方法の１つ（「パスワードフロー」と呼ばれる）では、フォームフィールドとしてusernameとpasswordを送信する必要があります。

