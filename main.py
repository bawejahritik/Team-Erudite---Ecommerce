from typing import Union
from environs import Env
from datetime import datetime
from fastapi import FastAPI
from fastapi import HTTPException
from models import allModels
from uuid import uuid4
from typing import Optional
import os
import motor.motor_asyncio
env = Env()
env.read_env()
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db=client.EruditeStore

store_collection = db.get_collection("stores")
user_collection = db.get_collection("users")
product_collection = db.get_collection("products")
order_collection = db.get_collection("orders")
inventory_collection = db.get_collection("inventory")

app = FastAPI()


@app.get("/healthz")
def read_root():
    return {"message":"Everything good"}

# Routes for User
    
@app.post("/user")
async def create_user(user: allModels.UserCreate):
    user_data = user.model_dump()
    try:
        user_data["user_id"] = str(uuid4())
        user_data["created_at"] = user_data["updated_at"] = str(datetime.now())
        user_preview = await user_collection.insert_one(user_data)
        del user_data["_id"]
        return user_data
    except:
        raise HTTPException(status_code=500, detail="Failed to create user")

@app.get("/users")
async def get_users():
    try:
        cursor = user_collection.find() 
        user_list = [
            {key: value for key, value in user.items() if key != '_id'}
            async for user in cursor
        ]
        return {"users": user_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unable to fetch Users: {str(e)}")

@app.put("/user/{user_id}")
async def update_user(user_id: str, user_data:allModels.UserUpdate):
    try:
        existing_user = await user_collection.find_one({"user_id":user_id})
        if(existing_user):
            del existing_user["_id"]
            update_data = user_data.model_dump()
            for key in update_data:
                if(update_data[key] is not None):
                    existing_user[key] = update_data[key]
            existing_user["updated_at"] = datetime.now()
            result = await user_collection.update_one(
                {"user_id":user_id},
                {"$set":existing_user}
            )
            if result.matched_count > 0:
                return {
                    "message":"User updated successfully",
                    "user":existing_user
                }                       
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except:
        raise HTTPException(status_code=500, detail="Unable to update user")
    
# Store Routes

@app.get("/stores")
async def get_store_list():
    try:
        cursor = store_collection.find() 
        store_list = [
            {key: value for key, value in store.items() if key != '_id'}
            async for store in cursor
        ]
        return {"users": store_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unable to fetch Stores: {str(e)}")

@app.post("/store")
async def create_store(store_data:allModels.Store):
    try:
        store_data = store_data.model_dump()
        store_data["created_at"] = store_data["updated_at"] = str(datetime.now())
        store_data["store_id"] = str(uuid4())
        result = await store_collection.insert_one(store_data)
        del store_data["_id"]
        return store_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create store: {str(e)}")
    
@app.delete("/store/{store_id}")
async def delete_store(store_id: str):
    try:
        result = await store_collection.delete_one({"store_id":store_id})
        if result.deleted_count > 0:
            return {
                "message":"Store deleted successfully"
            }
        else:
            return {
                "message":"Store not found"
            }
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")

@app.get("/products")
async def product_list(store_id: Optional[str] = None):
    try:
        if(store_id is not None):
            cursor = product_collection.find({"store_id":store_id}) 
        else:
            cursor = product_collection.find()
        product_list = [
            {key: value for key, value in product.items() if key != '_id'}
            async for product in cursor
        ]
        return {"users": product_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unable to fetch Stores: {str(e)}")

@app.post("/product")
async def create_product(product_data:allModels.ProductCreate):
    try:
        product_data = product_data.model_dump()
        product_data["uid"] = str(uuid4())
        product_data["created_at"] = product_data["updated_at"] = str(datetime.now())
        result =await product_collection.insert_one(product_data)
        del product_data["_id"]
        return {
            "message": "product created successfully",
            "product": product_data
        }
    except:
        raise HTTPException(status_code=500, detail="Failed to create product")

@app.put("/product/{product_id}")
async def update_product(product_id: str, product_data:allModels.ProductUpdate):
    try:
        print('')
        product_data = product_data.model_dump()
        product_data["updated_at"] = str(datetime.now())
        result = product_collection.find_one_and_update(
            {"uid":product_id},
            {"$set":product_data}
        )
        if(result.matching_count > 0):
            return {
                "message": "Product updated successfully"
            }
        else:
            return {
                "error": "Product not found"
            }
    except:
        raise HTTPException(status_code=500, detail="Failed to update product")

@app.delete("/product/{product_id}")
async def delete_product(product_id:str):
    try:
        result = product_collection.delete_one({"uid":product_id})
        if result.matched_count > 0:
            return {
                "message":"Product deleted successfully"
            }
        else:
            return {
                "message":"Product not found"
            }
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")