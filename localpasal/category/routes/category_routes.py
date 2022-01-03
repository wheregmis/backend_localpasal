from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth.auth_jwt import AuthJWT
from starlette import status

from configs.database import mongodatabase
from localpasal.global_schemas import serializeDict, serializeList
from bson import ObjectId
from ..models.category_model import Category
from localpasal.authentication import Hash

router = APIRouter(
    prefix="/category",
    tags=['Categories']
)


@router.get('/')
async def find_all_categories(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    print(Authorize.get_jwt_subject())
    return serializeList(mongodatabase.category.find())


@router.get('/{id}')
async def find_one_category(id, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return serializeDict(mongodatabase.category.find_one({"_id":ObjectId(id)}))


@router.post('/')
async def create_category(category: Category,  Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    mongodatabase.category.insert_one(dict(category))
    return jsonable_encoder({"category":category})

#
# @router.put('/{id}')
# async def update_user(id,user: User, Authorize:AuthJWT=Depends()):
#     try:
#         Authorize.jwt_required()
#
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid Token"
#         )
#     mongodatabase.user.find_one_and_update({"_id":ObjectId(id)},{
#         "$set":dict(user)
#     })
#     return serializeDict(mongodatabase.user.find_one({"_id":ObjectId(id)}))
#
#
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