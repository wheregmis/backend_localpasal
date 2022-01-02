from typing import Optional

from pydantic import BaseModel

from localpasal.authentication import Hash, Login


class User(BaseModel):
    mobileNumber: str
    emailAddress: str
    fullName: str
    city: str
    states: str
    country: str
    address: str
    lattitude: float
    longitude: float
    password: Optional[str]


def userFromUserModel(user: User):
    return infoFromUserModel(user), Login(email=user.emailAddress, password=Hash.bcrypt(user.password))


def infoFromUserModel(user: User):
    return User(
        mobileNumber=user.mobileNumber,
        emailAddress=user.emailAddress,
        fullName=user.fullName,
        city=user.city,
        states=user.states,
        country=user.country,
        address=user.address,
        lattitude=user.lattitude,
        longitude=user.longitude,
    )
