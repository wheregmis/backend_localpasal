from pydantic import BaseModel


class SignUpModel(BaseModel):
    email: str
    password: str
