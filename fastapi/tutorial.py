from fastapi import FastAPI, Query, Path, Body    
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl

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