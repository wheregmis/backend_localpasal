from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth.auth_jwt import AuthJWT
from starlette import status

from configs.database import mongodatabase
from localpasal.global_schemas import serializeDict, serializeList
from bson import ObjectId
from ..schemas.user_schemas import SignUpModel
from localpasal.user import User
from localpasal.authentication import Hash
from ..repository.user_repository import add_user

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
async def create_user(user: SignUpModel, background_tasks: BackgroundTasks):
    user = serializeDict(mongodatabase.authentication.find_one({"email": user.email}))
    if user['email']:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User Already Exists")
    mongodatabase.authentication.insert_one(dict(SignUpModel(email=user.email, password=Hash.bcrypt(user.password))))
    user_info = serializeDict(mongodatabase.authentication.find_one({"email": user.email}))
    background_tasks.add_task(add_user(dict(User(emailAddress=user.email))))
    return jsonable_encoder({"user":User(emailAddress=user.email)})


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