from pydantic import BaseModel, Field, EmailStr

from typing import Optional, List

from .poll import PollOut


class UserLogin(BaseModel):
    username: str = Field(
        min_length=3, max_length=50
    )
    password: str = Field(
        min_length=3, max_length=50
    )

    class Config:
        orm_mode = True


class UserChange(UserLogin):
    email: EmailStr = Field(
        min_length=3, max_length=50
    )


class UserIn(UserChange):
    admin_token: Optional[str] = Field(
        default=None, min_length=3, max_length=50
    )


class UserOut(UserIn):
    role: str = Field(
        min_length=3, max_length=50, default='user'
    )
    polls: Optional[List[PollOut]]


class User(UserOut):
    id: int



