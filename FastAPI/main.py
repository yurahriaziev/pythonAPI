from fastapi import FastAPI

app = FastAPI()

inventory = {
    1:{
        'name':'Milk',
        'price':3.99,
        'brand':'Regular'
    }
}

# passing multiple arguments into API end point
@app.get("/get-item/{item_id}/{name}")
def get_item(item_id: int, name: str):
    return inventory[item_id]