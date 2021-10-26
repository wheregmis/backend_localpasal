from fastapi import APIRouter, Depends
from models.products import Product 
from configs.database import conn, mongodatabase 
from schemas import users_schemas
from routers.authentication import oauth2
from schemas.users_schemas import serializeDict, serializeList
from bson import ObjectId
product = APIRouter(
    prefix="/product",
    tags=['Products']
) 

@product.get('/')
async def find_all_products(current_user: users_schemas.serializeDict = Depends(oauth2.get_current_user)):
    return serializeList(mongodatabase.product.find())

@product.get('/{id}')
async def find_one_product(id, current_user: users_schemas.serializeDict = Depends(oauth2.get_current_user)):
    return serializeDict(mongodatabase.product.find_one({"_id":ObjectId(id)}))

@product.post('/')
async def create_product(product: Product, current_user: users_schemas.serializeDict = Depends(oauth2.get_current_user)):
    mongodatabase.product.insert_one(dict(product))
    return serializeList(mongodatabase.product.find())

@product.put('/{id}')
async def update_product(id,product: Product, current_user: users_schemas.serializeDict = Depends(oauth2.get_current_user)):
    mongodatabase.product.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(product)
    })
    return serializeDict(mongodatabase.product.find_one({"_id":ObjectId(id)}))

@product.delete('/{id}')
async def delete_product(id,product: Product, current_user: users_schemas.serializeDict = Depends(oauth2.get_current_user)):
    return serializeDict(mongodatabase.product.find_one_and_delete({"_id":ObjectId(id)}))