from pydantic import BaseModel

class UserLogin(BaseModel):
    email: str 
    password: str


class UserSignup(BaseModel):
    username: str 
    email: str 
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
