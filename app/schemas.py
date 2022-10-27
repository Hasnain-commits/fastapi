from pydantic import BaseModel, EmailStr
from datetime import datetime

#Posts schemas

class Post_Base(BaseModel):
    title: str
    content: str
    published: bool = True


class Post_Create(Post_Base):
    pass


class Post_Response(Post_Base):
    id: int 
    created_at: datetime


#User schemas

class User_Create(BaseModel):
    email: EmailStr
    password: str


class User_Login(BaseModel):
    email: EmailStr
    password: str






