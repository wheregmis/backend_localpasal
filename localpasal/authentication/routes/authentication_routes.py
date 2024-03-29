from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

import datetime

from configs.database import mongodatabase
from localpasal.authentication import Login
from localpasal.authentication import Hash
from localpasal.global_schemas import serializeDict

router = APIRouter(tags=['Authentication'])


@router.post('/login')
async def login(loginUser: Login, Authorize: AuthJWT = Depends()):
    """
    This route logs in the user
    :param loginUser:
    :param Authorize:
    :return: {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "user": user_info}
    """
    user = mongodatabase.authentication.find_one({"email": loginUser.email})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User not found")
    new_user = serializeDict(user)
    if not Hash.verify(new_user['password'], loginUser.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
    user_info = serializeDict(mongodatabase.user.find_one({"emailAddress": loginUser.email}))
    expires = datetime.timedelta(days=1)
    test = datetime.datetime.now() + datetime.timedelta(days=1)
    expire_timestamp = (datetime.datetime.timestamp(test))
    access_token = Authorize.create_access_token(subject=user['email'], expires_time=expires)
    refresh_token = Authorize.create_refresh_token(subject=user['email'])
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "expires_at": expire_timestamp, "user": user_info}


# refreshing tokens

@router.get('/refresh')
async def refresh_token(Authorize: AuthJWT = Depends()):
    """
    ## Create a fresh token
    This creates a fresh token. It requires an refresh token.
    Bearer JWTToken
    """
    try:
        Authorize.jwt_refresh_token_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Please provide a valid refresh token"
                            )
    print('Refreshed')
    current_user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=current_user)
    return jsonable_encoder({"access": access_token})

