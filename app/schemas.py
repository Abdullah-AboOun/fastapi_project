from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserReturn(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostReturn(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserReturn

    class Config:
        orm_mode = True


class PostReturnWVote(BaseModel):
    Post: PostReturn
    votes: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1, ge=0)  # type: ignore
