from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TokenModel(BaseModel):
    access_token: str
    token_type: str

class UserCreatedModel(BaseModel):
    id: int

class PostCreatedModel(BaseModel):
    id: int

class LikeCreateDeleteModel(BaseModel):
    user_id: int
    post_id: int

class UserModel(BaseModel):
    email: str
    created_at: datetime
    last_login_at: Optional[datetime] = None
    last_request_at: Optional[datetime] = None


class UserInDbModel(UserModel):
    id: int
    password_hash: str


class UserCreateModel(BaseModel):
    email: str
    password: str


class UserActivityModel(BaseModel):
    last_login_at: Optional[datetime] = None
    last_request_at: Optional[datetime] = None


class PostCreateModel(BaseModel):
    ...


# class LikeCreateDeleteModel(BaseModel):
#     post_id: int
#     user_id: Optional[int] = None
