# app/schemas.py
from pydantic import BaseModel

class StoryBase(BaseModel):
    title: str
    description: str
    category: str

class StoryCreate(StoryBase):
    pass

class Story(StoryBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True