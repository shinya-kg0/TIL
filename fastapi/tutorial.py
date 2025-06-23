from fastapi import FastAPI, Query, Path, Body, Cookie, Header, status, Form
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Annotated, Any

class ModelName(str, Enum):
    resnet = "resnet"
    t5 = "t5"
    visiontransformer = "visiontransformer"
    
class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: str | None = Field(
        # 追加引数として、exampleを設定できる
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None    # dict[int, float]も使用可能
    tags: set[str] = set()
    image: list[Image] | None = None
    
class User(BaseModel):
    username: str
    full_name: str | None = None
    
class Cookies(BaseModel):
    # 受け付けるCookieを制限する
    model_config = {"extra": "forbid"}

    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None
    
class CommonHeaders(BaseModel):
    model_config = {"extra": "forbid"}
    
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []
    
class FormData(BaseModel):
    model_config = {"extra": "forbid"}
    username: str
    password: str
    
# ここら辺は次のようにリファクタできる！
# class UserIn(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     full_name: str | None = None
    
# class UserOut(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None

# class UserInDB(BaseModel):
#     username: str
#     hashed_password: str
#     email: EmailStr
#     full_name: str | None = None

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
    
class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.resnet:
        return {"model_name": model_name, "message": "This is resnet!"}
    else:
        pass

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    item: Item,
    user: User,
    importance: int = Body(embed=True),    # embed=Trueで単一のボディパラメータを埋め込める
    q: str | None = None):
    result = {"item_id": item_id, **item.dict(), "user": user}
    if q:
        result.update({"q": q})
    if item:
        result.update({"item": item})
    return result

@app.get("/items/")
async def read_items(
    q: list[str] | None = Query(
        default=None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=2, max_length=50),
        # deprecated=True を指定すると非推奨パラメータであることを明示できる。らしい？？
    ):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
# pattern="^fixedquary$"で正規表現を利用可能

@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get", gt=0, le=1000),
    q: str | None = Query(default=None, alias="item-quary"),
    size: float = Query(gt=0, lt=10.5),
    ):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# 各種型ヒントの使い方
@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}

@app.get("/items/")
async def read_items(
    strange_header: Annotated[str | None, Header(default=True, convert_underscores=False)] = None
):
    return {"strange_header": strange_header}

@app.get("/items/")
async def read_items(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X_Token values": x_token}

@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookies()]):
    return cookies

@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers

# これはアンチパターン
@app.post("/user/")
async def create_user(user: UserIn) -> UserIn:
    return user

# これだとレスポンスとしてパスワードが漏れることはない
@app.post("/user/", response_model=UserOut, response_model_exclude_unset=True)
async def create_user(user: UserIn) -> Any:
    return user

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}

@app.post("/login/")
async def login(user_name: str = Form(), password: str = Form()):
    return {"user_name": user_name}

@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data
