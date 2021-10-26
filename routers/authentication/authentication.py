from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models import products, users
from configs.database import conn, mongodatabase 
from routers.authentication.hashing import Hash
from routers.authentication import token
from schemas.users_schemas import serializeDict, serializeList
from bson import ObjectId
from sqlalchemy.orm import Session
router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends()):
    user = serializeDict(mongodatabase.user.find_one({"email":request.username}))
    print(request.username)
    print(user)
    if not user['email']:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(user['password'], request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
    

    access_token = token.create_access_token(data={"sub": user['email']})
    return {"access_token": access_token, "token_type": "bearer", "user": user}