from fastapi import APIRouter, Depends
from models.users import User 
from configs.database import conn, mongodatabase 
from schemas import users_schemas
from routers.authentication import oauth2
from schemas.users_schemas import serializeDict, serializeList
from bson import ObjectId
from routers.authentication.hashing import Hash


user = APIRouter(
    prefix="/user",
    tags=['Users']
) 

@user.get('/')
async def find_all_users(current_user: users_schemas.serializeDict = Depends(oauth2.get_current_user)):
    return serializeList(mongodatabase.user.find())

# @user.get('/{id}')
# async def find_one_user(id):
#     return serializeDict(mongodatabase.local.user.find_one({"_id":ObjectId(id)}))

@user.post('/')
async def create_user(user: User):
    # need to pass new_user to encrypt password however having issue with bycrpt
    new_user = User(name=user.name,email=user.email,password=Hash.bcrypt(user.password))
    mongodatabase.user.insert_one(dict(new_user))
    return serializeList(mongodatabase.user.find())

@user.put('/{id}')
async def update_user(id,user: User, current_user: users_schemas.serializeDict = Depends(oauth2.get_current_user)):
    mongodatabase.user.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(user)
    })
    return serializeDict(mongodatabase.user.find_one({"_id":ObjectId(id)}))

@user.delete('/{id}')
async def delete_user(id,user: User, current_user: users_schemas.serializeDict = Depends(oauth2.get_current_user)):
    return serializeDict(mongodatabase.user.find_one_and_delete({"_id":ObjectId(id)}))