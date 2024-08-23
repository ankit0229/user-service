from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    address: Optional[str] = None
    date_of_birth: Optional[str] = None
    password: str = Field(min_length=6)


class UserProfile(BaseModel):
    email: EmailStr
    name: str
    address: Optional[str] = None
    date_of_birth: Optional[str] = None

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[str] = None

