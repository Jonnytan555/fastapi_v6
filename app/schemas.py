from typing import Optional, List
from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class ConfigFromOrm:
    model_config = {"from_attributes": True}  # pydantic v2

# ---------- Users ----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    class Config(ConfigFromOrm): ...

class UserLoginJSON(BaseModel):
    username: EmailStr
    password: str

# ---------- Auth ----------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    id: Optional[int] = None

# ---------- Posts ----------
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserResponse
    class Config(ConfigFromOrm): ...


class PostOut(PostBase):
    Post: Post
    votes: int
    class Config(ConfigFromOrm): ...

# ---------- Votes ----------
class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1, ge=0)]
