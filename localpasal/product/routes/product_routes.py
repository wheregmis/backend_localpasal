import datetime

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth.auth_jwt import AuthJWT
from starlette import status

from configs.database import mongodatabase
from localpasal.global_schemas import serializeDict, serializeList
from bson import ObjectId
from ..models.product_model import Product

router = APIRouter(
    prefix="/product",
    tags=['Products']
)


@router.get('/')
async def find_all_products():
    return serializeList(mongodatabase.product.find())


@router.get('/{id}')
async def find_one_product(id):
    return serializeDict(mongodatabase.product.find_one({"_id":ObjectId(id)}))


@router.post('/')
async def create_product(product: Product, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    print("Testing CICD")
    product_id = mongodatabase.product.insert_one(dict(product)).inserted_id
    return serializeDict(mongodatabase.product.find_one({"_id":ObjectId(product_id)}))


@router.put('/{id}')
async def update_product(id,product: Product, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    mongodatabase.product.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(product)
    })
    return serializeDict(mongodatabase.user.find_one({"_id":ObjectId(id)}))


# @router.delete('/{id}')
# async def delete_user(id,user: User, Authorize:AuthJWT=Depends()):
#     try:
#         Authorize.jwt_required()
#
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid Token"
#         )
#     return serializeDict(mongodatabase.user.find_one_and_delete({"_id":ObjectId(id)}))