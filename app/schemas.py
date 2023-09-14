
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, conint


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int]
    # created_at: datetime

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    User_id: int
    created_at: datetime
    owner: UserOut

    class Config:
        from_attributes = True  # orm_mode changed to from_attributes in V2 pydantic


class PostOut (BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # specifies less than 1, make  0 or 1 if possible
