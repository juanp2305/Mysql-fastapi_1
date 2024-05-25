from typing import Optional, Union
from fastapi import Form
from pydantic import BaseModel

class Users(BaseModel):
    username:  str | None = None
    password:  str | None = None

class Login(BaseModel):
    username:  str = Form()
    password:  str = Form()
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
   

    
    