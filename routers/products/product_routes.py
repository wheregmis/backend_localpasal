from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth.auth_jwt import AuthJWT
from starlette import status
from models.products import Product 
from configs.database import mongodatabase 
from schemas.users_schemas import serializeDict, serializeList
from bson import ObjectId
product = APIRouter(
    prefix="/product",
    tags=['Products']
) 

@product.get('/')
async def find_all_products(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return serializeList(mongodatabase.product.find())

@product.get('/{id}')
async def find_one_product(id, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return serializeDict(mongodatabase.product.find_one({"_id":ObjectId(id)}))

@product.post('/')
async def create_product(product: Product, Authorize:AuthJWT=Depends()):
    mongodatabase.product.insert_one(dict(product))
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return serializeList(mongodatabase.product.find())

@product.put('/{id}')
async def update_product(id,product: Product, Authorize:AuthJWT=Depends()):
    mongodatabase.product.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(product)
    })
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return serializeDict(mongodatabase.product.find_one({"_id":ObjectId(id)}))

@product.delete('/{id}')
async def delete_product(id,product: Product, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return serializeDict(mongodatabase.product.find_one_and_delete({"_id":ObjectId(id)}))