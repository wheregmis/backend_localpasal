from typing import Optional
from localpasal.authentication import Hash
from pydantic import BaseModel


class User(BaseModel):
    userId: Optional[str]
    fullName: Optional[str]
    emailAddress: str
    userType: Optional[str]
    userPanNo: Optional[str]
    userContactNumber: Optional[str]
    address: Optional[str]
    userLocLatitude: Optional[str]
    userLocLongitude: Optional[str]
    password: Optional[str]


def user_from_signup_model(user: User):
    return User(
        emailAddress=user.emailAddress,
        password=Hash.bcrypt(user.password)
    )


def little_info_from_user(user: User):
    return User(
        userId=user.userId,
        emailAddress=user.emailAddress,
        fullName=user.fullName,
        address=user.address,
    )
