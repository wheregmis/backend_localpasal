from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth.auth_jwt import AuthJWT
from starlette import status
from models.users import User 
from configs.database import mongodatabase 
from schemas.users_schemas import serializeDict, serializeList
from bson import ObjectId
from routers.authentication.hashing import Hash


user = APIRouter(
    prefix="/user",
    tags=['Users']
) 

@user.get('/')
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

@user.get('/{id}')
async def find_one_user(id, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return serializeDict(mongodatabase.local.user.find_one({"_id":ObjectId(id)}))

@user.post('/')
async def create_user(user: User):
    # need to pass new_user to encrypt password however having issue with bycrpt
    new_user = User(name=user.name,email=user.email,password=Hash.bcrypt(user.password))
    mongodatabase.user.insert_one(dict(new_user))
    return serializeList(mongodatabase.user.find())

@user.put('/{id}')
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

@user.delete('/{id}')
async def delete_user(id,user: User, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return serializeDict(mongodatabase.user.find_one_and_delete({"_id":ObjectId(id)}))