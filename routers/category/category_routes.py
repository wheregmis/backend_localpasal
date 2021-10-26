from fastapi import APIRouter, Depends
from models.category import Category 
from configs.database import conn, mongodatabase 
from schemas import category_schemas
from routers.authentication import oauth2
from schemas.users_schemas import serializeDict, serializeList
from bson import ObjectId
category = APIRouter(
    prefix="/category",
    tags=['Category']
) 

@category.get('/')
async def find_all_categories(current_user: category_schemas.serializeDict = Depends(oauth2.get_current_user)):
    return serializeList(mongodatabase.category.find())

@category.get('/{id}')
async def find_one_category(id, current_user: category_schemas.serializeDict = Depends(oauth2.get_current_user)):
    return serializeDict(mongodatabase.category.find_one({"_id":ObjectId(id)}))

@category.post('/')
async def create_category(category: Category, current_user: category_schemas.serializeDict = Depends(oauth2.get_current_user)):
    mongodatabase.category.insert_one(dict(category))
    return serializeList(mongodatabase.category.find())

@category.put('/{id}')
async def update_category(idcategory: Category, current_user: category_schemas.serializeDict = Depends(oauth2.get_current_user)):
    mongodatabase.category.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(category)
    })
    return serializeDict(mongodatabase.category.find_one({"_id":ObjectId(id)}))

@category.delete('/{id}')
async def delete_category(id,category: Category, current_user: category_schemas.serializeDict = Depends(oauth2.get_current_user)):
    return serializeDict(mongodatabase.category.find_one_and_delete({"_id":ObjectId(id)}))