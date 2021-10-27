from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from configs.database import conn, mongodatabase 
from routers.authentication.hashing import Hash
from schemas.schemas import Login, RefreshToken
from schemas.users_schemas import serializeDict, serializeList
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(loginUser:Login,Authorize:AuthJWT=Depends()):
    user = serializeDict(mongodatabase.user.find_one({"email":loginUser.email}))
    if not user['email']:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(user['password'], loginUser.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
    

    access_token = Authorize.create_access_token(subject=user['email'])
    refresh_token = Authorize.create_refresh_token(subject=user['email'])
    return {"access_token": access_token,"refresh_token": refresh_token, "token_type": "bearer", "user": user}



#refreshing tokens

@router.get('/refresh')
async def refresh_token(Authorize:AuthJWT=Depends()):
    """
    ## Create a fresh token
    This creates a fresh token. It requires an refresh token.
    """
    try:
        Authorize.jwt_refresh_token_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please provide a valid refresh token"
        ) 

    current_user=Authorize.get_jwt_subject()
    access_token=Authorize.create_access_token(subject=current_user)
    return jsonable_encoder({"access":access_token})

