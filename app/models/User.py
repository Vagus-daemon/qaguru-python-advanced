from pydantic import EmailStr, BaseModel, HttpUrl
from sqlmodel import Field, SQLModel
from typing import Optional


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    avatar: Optional[str]


class UserCreate(BaseModel):
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    avatar: Optional[HttpUrl]


class UserUpdate(BaseModel):
    email: Optional[EmailStr] | None = None
    first_name: Optional[str] | None = None
    last_name: Optional[str] | None = None
    avatar: Optional[HttpUrl] | None = None
