from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime

# ---------- Users ----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

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

    model_config = ConfigDict(from_attributes=True)


class PostOut(BaseModel):
    Post: Post
    votes: int

    model_config = ConfigDict(from_attributes=True)

# ---------- Votes ----------
class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1, ge=0)]
