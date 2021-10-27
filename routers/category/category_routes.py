from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth.auth_jwt import AuthJWT
from starlette import status
from models.category import Category 
from configs.database import mongodatabase 
from routers.authentication import oauth2
from schemas.users_schemas import serializeDict, serializeList
from bson import ObjectId
category = APIRouter(
    prefix="/category",
    tags=['Category']
) 

@category.get('/')
async def find_all_categories(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return serializeList(mongodatabase.category.find())

@category.get('/{id}')
async def find_one_category(id, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return serializeDict(mongodatabase.category.find_one({"_id":ObjectId(id)}))

@category.post('/')
async def create_category(category: Category, Authorize:AuthJWT=Depends()):
    mongodatabase.category.insert_one(dict(category))
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return serializeList(mongodatabase.category.find())

@category.put('/{id}')
async def update_category(idcategory: Category, Authorize:AuthJWT=Depends()):
    mongodatabase.category.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(category)
    })
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return serializeDict(mongodatabase.category.find_one({"_id":ObjectId(id)}))

@category.delete('/{id}')
async def delete_category(id,category: Category, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return serializeDict(mongodatabase.category.find_one_and_delete({"_id":ObjectId(id)}))