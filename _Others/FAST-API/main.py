from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()
class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None
     
inventory = {}

# @app.get("/get-item/{item_id}")
# def get_item(item_id: int = Path(None, description="The id of item you looked for", gt=0)):
#     return inventory[item_id]

@app.get("/get-by-name")
def get_item(*, item_id:int,name: Optional[str] = None, test: int):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID not found.") # return {"Data": "item not found"}} # 

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item ID not exist.")
    
    inventory[item_id] = item
    # {"name": item.name, "brand": item.brand, "price": item.price}
    return inventory[item_id]  

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID not found.")
    
    if item.name != None:
        inventory[item_id].name = item.name
    if item.price != None:
        inventory[item_id].price = item.price
    if item.brand != None:
        inventory[item_id].brand = item.brand
        
    return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item to delete", gt=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID not found.")
    
    del inventory[item_id]
    return {"Succes": "Item deleted!"}
# http://127.0.0.1:8000/get-by-name?name=Milk
# http://127.0.0.1:8000/get-by-name?test=2&name=Milk

# uvicorn main:app --reload (to run)
# API - aplication programming interface, web service that provides interface to apps to manipulate and retrives infos. 
# Api connects frontend anad backend of app together