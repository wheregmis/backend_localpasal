from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth.auth_jwt import AuthJWT
from starlette import status

from configs.database import mongo_database as mongodatabase
from localpasal.global_schemas import serializeDict, serializeList
from bson import ObjectId
from localpasal.authentication import Login
from localpasal.user import User, userFromUserModel, infoFromUserModel



router = APIRouter(
    prefix="/user",
    tags=['Users']
) 

@router.get('/')
async def find_all_users(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    print(Authorize.get_jwt_subject())
    return serializeList(mongodatabase.user.find())

@router.get('/{id}')
async def find_one_user(id, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return serializeDict(mongodatabase.user.find_one({"_id":ObjectId(id)}))

@router.post('/')
async def create_user(user: User):
    # need to pass new_user to encrypt password however having issue with bycrpt
    new_user, authentication_user = userFromUserModel(user)
    mongodatabase.authentication.insert_one(dict(authentication_user))
    mongodatabase.user.insert_one(dict(new_user))
    return jsonable_encoder({"user":new_user})

@router.put('/{id}')
async def update_user(id,user: User, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    mongodatabase.user.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(user)
    })
    return serializeDict(mongodatabase.user.find_one({"_id":ObjectId(id)}))

@router.delete('/{id}')
async def delete_user(id,user: User, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return serializeDict(mongodatabase.user.find_one_and_delete({"_id":ObjectId(id)}))