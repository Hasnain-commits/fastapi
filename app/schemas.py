from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

# User schemas


class User_Base(BaseModel):
    id: int
    email: EmailStr


class User_Create(User_Base):
    pass


class User_Login(User_Base):
    pass

# Posts schemas


class Post_Base(BaseModel):
    title: str
    content: str
    published: bool = True


class Post_All(Post_Base):
    user_id: int
    email: EmailStr
    post_id: int


class Post_Create(Post_Base):
    pass


class Post_Response(Post_Base):
    post_likes: int
    pass

# JWT Token


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    vote_dir: conint(le=1)
