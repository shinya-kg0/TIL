from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

class ModelName(str, Enum):
    resnet = "resnet"
    t5 = "t5"
    visiontransformer = "visiontransformer"

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

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
    return item

